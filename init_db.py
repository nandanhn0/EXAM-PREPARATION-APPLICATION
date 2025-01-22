from app import db  # Import db from the app
from app import User, Document  # Import models

# Create the tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
