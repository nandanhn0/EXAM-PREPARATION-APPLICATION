import io
import os
import unittest

from app import app, db, StudyMaterial, allowed_file, get_search_suggestions


class ExamPrepAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            get_search_suggestions.cache_clear()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            get_search_suggestions.cache_clear()

    def test_allowed_file_checks_extensions(self):
        self.assertTrue(allowed_file("notes.pdf"))
        self.assertFalse(allowed_file("notes.exe"))

    def test_search_api_returns_suggestions(self):
        with app.app_context():
            db.session.add(StudyMaterial(filename="Algorithms_Notes.pdf", file_path="static/uploads/Algorithms_Notes.pdf"))
            db.session.add(StudyMaterial(filename="Algebra_Basics.pdf", file_path="static/uploads/Algebra_Basics.pdf"))
            db.session.commit()

        response = self.client.get("/api/search_suggestions?query=alg")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Algorithms_Notes.pdf", response.get_json())

    def test_upload_uses_custom_name(self):
        response = self.client.post(
            "/upload",
            data={
                "file_name": "My Notes",
                "file": (io.BytesIO(b"sample data"), "source.pdf"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 302)

        with app.app_context():
            stored = StudyMaterial.query.first()
            self.assertIsNotNone(stored)
            self.assertTrue(stored.filename.lower().startswith("my_notes"))
            if os.path.exists(stored.file_path):
                os.remove(stored.file_path)


if __name__ == "__main__":
    unittest.main()
