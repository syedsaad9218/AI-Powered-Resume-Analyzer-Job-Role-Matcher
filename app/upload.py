import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

def allowed_file(filename):
    """Check whether file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file, upload_path):
    if file.filename == "":
        return (False, "No file selected.")

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        return (True, filename)

    return (False, "Invalid file type. Please upload a .pdf, .doc, or .docx.")
