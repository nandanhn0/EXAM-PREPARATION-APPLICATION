class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///documents.db'  # For SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
