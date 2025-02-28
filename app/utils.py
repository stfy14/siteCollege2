import os
from werkzeug.utils import secure_filename

def save_uploaded_file(file, upload_folder, allowed_extensions):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    if file and allowed_file(file.filename, allowed_extensions):
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename
    return None

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(filename):
    base_name = secure_filename(filename).rsplit('.', 1)[0]
    extension = secure_filename(filename).rsplit('.', 1)[1]
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}.{extension}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1
