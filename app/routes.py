from flask import Blueprint, render_template, request, abort
from flask import current_app
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

        # Начинаем запрос по опубликованным работам
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
