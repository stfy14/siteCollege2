import os
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """Проверяет, разрешён ли тип файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, upload_folder, allowed_extensions):
    """Сохраняет загруженный файл, если его тип разрешён."""
    if file and allowed_file(file.filename, allowed_extensions):
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return filename  # можно вернуть file_path, если это необходимо
    return None
