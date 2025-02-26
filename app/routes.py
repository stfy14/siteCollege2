from flask import Blueprint, render_template, request, abort
from app.models import Work
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')

    # Используем filter_by для простоты
    query = Work.query.filter_by(is_published=True)

    if search_query:
        query = query.filter(Work.title.ilike(f'%{search_query}%'))

    works = query.paginate(page=page, per_page=9)
    return render_template('index.html', works=works, search_query=search_query)

@main_bp.route('/work/<int:work_id>')
def work_details(work_id):
    work = Work.query.get_or_404(work_id)
    if not work.is_published:
        abort(404)
    return render_template('work.html', work=work)
