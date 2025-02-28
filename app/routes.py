from flask import Blueprint, render_template, request, abort, redirect, url_for
from flask import current_app
from app.utils import save_uploaded_file
from app.models import Work
from app import db
from sqlalchemy.exc import OperationalError
from sqlalchemy import inspect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        inspector = inspect(db.engine)
        if not inspector.has_table('works'):
            current_app.logger.info('Table "work" does not exist')
            return render_template('index.html', 
                                    works=None)

        page = request.args.get('page', 1, type=int)
        search_query = request.args.get('search', '')
        award_filter = request.args.get('award', '')
        direction_filter = request.args.get('direction', '')
        university_filter = request.args.get('university', '')

        query = Work.query.filter_by(is_published=True)

        if search_query:
            query = query.filter(Work.title.ilike(f'%{search_query}%'))

        if award_filter:
            query = query.filter(Work.award == award_filter)

        if direction_filter:
            query = query.filter(Work.direction == direction_filter)

        if university_filter:
            query = query.filter(Work.university == university_filter)

        works = query.paginate(page=page, per_page=9)
        return render_template('index.html', 
                            works=works, 
                            search_query=search_query,
                            award_filter=award_filter,
                            direction_filter=direction_filter,
                            university_filter=university_filter)
    
    except OperationalError as e:
        current_app.logger.error(f'Database error: {str(e)}')
        return render_template('index.html', works=None)
    except Exception as e:
        current_app.logger.error(f'Unexpected error: {str(e)}')
        return render_template('index.html', works=None)

@main_bp.route('/work/<int:work_id>')
def work_details(work_id):
    work = Work.query.get_or_404(work_id)
    if not work.is_published:
        abort(404)
    return render_template('work.html', work=work)

@main_bp.route('/upload', methods=['GET', 'POST'])
def upload_work():
    if request.method == 'POST':
        # Проверяем наличие файла в запросе
        if 'file' not in request.files:
            return "No file part", 400
            
        file = request.files['file']
        
        # Проверяем что файл был выбран
        if file.filename == '':
            return "No selected file", 400
            
        # Сохраняем файл
        filename = save_uploaded_file(
            file,
            current_app.config['UPLOAD_FOLDER'],
            current_app.config['ALLOWED_EXTENSIONS']
        )
        
        if filename:
            new_work = Work(
                title=request.form.get('title'),
                authors=request.form.get('authors'),
                description=request.form.get('description'),
                award=request.form.get('award'),
                university=request.form.get('university'),
                direction=request.form.get('direction'),
                file_path=f"uploads/{filename}" 
            )
            
            db.session.add(new_work)
            db.session.commit()
            
            return redirect(url_for('main.work_details', work_id=new_work.id))
        else:
            return "File upload failed", 400
        
    # GET запрос - показываем форму
    return render_template('upload.html')