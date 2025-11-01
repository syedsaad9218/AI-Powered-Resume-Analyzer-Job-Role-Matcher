import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    """Checks if the file's extension is in the allowed list."""""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_resume(file, upload_path):
    """
    Validates and saves a resume file.

    Args:
        file: The file object from the Flask request.
        upload_path: The path to the 'uploads' folder.

    Returns:
        A tuple (bool, str) representing (success, message_or_filename).
    """
    # Check if a file was actually selected
    if file.filename == '':
        return (False, 'No file selected.')

    # Check if the file type is allowed and save it
    if file and allowed_file(file.filename):
        # Sanitize the filename for security
        filename = secure_filename(file.filename)
        
        # Create the full path to save the file
        file_path = os.path.join(upload_path, filename)
        
        # Save the file
        file.save(file_path)
        
        # Return success status and the saved filename
        return (True, filename)
    else:
        # Return failure status and an error message
        return (False, 'Invalid file type. Please upload a .pdf, .doc, or .docx.')
