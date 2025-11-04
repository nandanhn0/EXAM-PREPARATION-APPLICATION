# Exam Preparation Application

This Flask-based web application allows students to upload, search, and download study materials. It's designed to be a centralized hub for accessing course-related documents, making exam preparation more efficient and organized.

## Features

- **File Upload**: Students can upload various file types, including PDF, DOCX, TXT, PPTX, and XLSX.
- **Search Functionality**: A powerful search feature allows users to quickly find specific study materials by filename.
- **Download Option**: Any uploaded document can be easily downloaded for offline access.
- **Organized by Semester**: The application includes a semester-based navigation system to help students find relevant materials for their current courses.

## Tech Stack

- **Framework**: Flask
- **Database**: SQLAlchemy with SQLite
- **Frontend**: HTML, CSS, JavaScript

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/exam-preparation-app.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd exam-preparation-app
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv myenv
   ```
4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```
5. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Run the application**:
   ```bash
   python app.py
   ```
7. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Uploading Files**: Click the "Upload" button to select and upload your study materials.
- **Searching for Files**: Use the search bar to find files by name.
- **Navigating by Semester**: Select your semester to view a list of relevant subjects and their corresponding study materials.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create an issue or submit a pull request.
