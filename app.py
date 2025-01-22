from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configurations for the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study_material.db'  # Database URI
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store uploaded files under 'static'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'pptx', 'xlsx'}  # Allowed file types
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model for storing study materials in the database
class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
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
    if file and allowed_file(file.filename):  # Validate file extension
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Save file details in the database
        new_file = StudyMaterial(filename=filename, file_path=filepath)
        db.session.add(new_file)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to homepage after upload
    return 'File type not allowed', 400

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to handle search requests
@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query')
    # Search the database for files matching the query
    results = StudyMaterial.query.filter(StudyMaterial.filename.ilike(f'%{query}%')).all()
    return render_template('search_results.html', results=results)

# Route for downloading files
@app.route('/download/<filename>')
def download_file(filename):
    # Send the file from the uploads folder to the user
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/search_documents', methods=['GET'])
def search_documents():
    query = request.args.get('query', '')  # Default to empty string if no query is provided
    if query:
        # If there is a query, filter the files based on the query
        results = StudyMaterial.query.filter(StudyMaterial.filename.ilike(f'%{query}%')).all()
    else:
        # If no query is provided, show all files
        results = StudyMaterial.query.all()
    
    return render_template('search_results.html', results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
