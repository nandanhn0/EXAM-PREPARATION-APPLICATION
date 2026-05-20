from functools import lru_cache
from flask import Flask, jsonify, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import time

MAX_UPLOAD_SIZE_MB = 16
SUGGESTION_CACHE_TTL_SECONDS = 60

app = Flask(__name__)

# Configurations for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_material.db'  # Database URI
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store uploaded files under 'static'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'pptx', 'xlsx'}  # Allowed file types
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE_MB * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60 * 60 * 24 * 30
db = SQLAlchemy(app)

# Model for storing study materials in the database
class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False, index=True)
    file_path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"StudyMaterial('{self.filename}', '{self.file_path}')"

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Create the database tables
with app.app_context():
    db.create_all()

# Route for the homepage with upload and search features
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)  # Redirect if no file is selected
    file = request.files['file']
    original_filename = secure_filename(file.filename)
    if file and allowed_file(original_filename):  # Validate file extension
        custom_name = secure_filename(request.form.get('file_name', '').strip())
        name_root, extension = os.path.splitext(original_filename)
        if custom_name:
            name_root = os.path.splitext(custom_name)[0] or name_root
        filename = get_unique_filename(f"{name_root}{extension.lower()}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Save file details in the database
        new_file = StudyMaterial(filename=filename, file_path=filepath)
        db.session.add(new_file)
        db.session.commit()
        get_search_suggestions.cache_clear()
        return redirect(url_for('index'))  # Redirect to homepage after upload
    return 'File type not allowed', 400

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_unique_filename(filename):
    name_root, extension = os.path.splitext(filename)
    unique_name = filename
    counter = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], unique_name)):
        unique_name = f"{name_root}_{counter}{extension}"
        counter += 1
    return unique_name

def normalize_query(raw_query):
    return (raw_query or '').strip()

@lru_cache(maxsize=256)
def get_search_suggestions(query, cache_bucket):
    normalized_query = query.lower()
    records = (
        db.session.query(StudyMaterial.filename)
        .filter(StudyMaterial.filename.ilike(f'%{normalized_query}%'))
        .order_by(StudyMaterial.filename.asc())
        .limit(8)
        .all()
    )
    return [record[0] for record in records]

# Route to handle search requests
@app.route('/search', methods=['GET'])
def search_files():
    query = normalize_query(request.args.get('query'))
    page = request.args.get('page', 1, type=int)
    materials_query = StudyMaterial.query
    if query:
        materials_query = materials_query.filter(StudyMaterial.filename.ilike(f'%{query}%'))
    pagination = materials_query.order_by(StudyMaterial.id.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('search_results.html', results=pagination.items, query=query, pagination=pagination)

# Route for downloading files
@app.route('/download/<filename>')
def download_file(filename):
    # Send the file from the uploads folder to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search_documents', methods=['GET'])
def search_documents():
    return redirect(url_for('search_files', query=normalize_query(request.args.get('query')), page=request.args.get('page', 1, type=int)))

@app.route('/api/search_suggestions', methods=['GET'])
def search_suggestions():
    query = normalize_query(request.args.get('query'))
    if len(query) < 2:
        return jsonify([])
    cache_bucket = int(time.time() // SUGGESTION_CACHE_TTL_SECONDS)
    return jsonify(get_search_suggestions(query, cache_bucket))

if __name__ == "__main__":
    app.run(debug=True)
