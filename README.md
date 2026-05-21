# Exam Preparation Application

Flask-based web app to upload study documents, search materials, and browse semester/subject/module resources.

## Local Setup

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Deploy (Render)

This repository is now deployment-ready for Render.

1. Push this branch to GitHub.
2. In Render, create a **New Web Service** from this repository.
3. Render will auto-detect `render.yaml` with:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. (Optional) set `DATABASE_URL` in Render if you want a managed database.

### Notes

- Without `DATABASE_URL`, the app uses local SQLite (`study_material.db`).
- Uploaded files are saved under `static/uploads`; on many cloud hosts this filesystem is ephemeral.

## What was optimized

- Added indexed filename lookups, paginated search results, and cached search suggestions API.
- Reduced frontend overhead by removing duplicated inline JavaScript and using one optimized static script.
- Improved upload behavior with custom display names and collision-safe filenames.
- Improved UI consistency with modernized shared styling, better spacing/contrast, and keyboard-visible focus states.
