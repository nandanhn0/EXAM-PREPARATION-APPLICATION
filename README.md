# Exam Preparation Application

Flask-based web app to upload study documents, search materials, and browse semester/subject/module resources.

## Setup

```bash
pip install flask flask_sqlalchemy
python app.py
```

Open `http://127.0.0.1:5000`.

## What was optimized

- Added indexed filename lookups, paginated search results, and cached search suggestions API.
- Reduced frontend overhead by removing duplicated inline JavaScript and using one optimized static script.
- Improved upload behavior with custom display names and collision-safe filenames.
- Improved UI consistency with modernized shared styling, better spacing/contrast, and keyboard-visible focus states.
