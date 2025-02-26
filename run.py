from app import create_app, db
import click

app = create_app()

@app.cli.command("init-db")
def init_db():
    """Инициализирует базу данных."""
    db.create_all()
    click.echo("Database initialized.")

@app.cli.command("add-sample-data")
def add_sample_data():
    """Добавляет пример записи в базу данных."""
    from app.models import Work
    with app.app_context():
        work = Work(
            title="Автоматизация проектирования в среде АКСПИСАЛ",
            authors="Тимонина А.В.",
            description="Освоение автономных казанков...",
            award="Диплом 1 степени",
            university="Волгоградский государственный технический университет",
            direction="Компьютерные системы"
        )
        db.session.add(work)
        db.session.commit()
        click.echo("Sample data added.")

if __name__ == '__main__':
    app.run(debug=True)
