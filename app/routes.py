from flask import Blueprint, render_template, request, abort
from app.models import Work
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
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

@main_bp.route('/work/<int:work_id>')
def work_details(work_id):
    work = Work.query.get_or_404(work_id)
    if not work.is_published:
        abort(404)
    return render_template('work.html', work=work)
