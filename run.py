from app import create_app, db
import click

app = create_app()

@app.cli.command("init-db")
def init_db():
    try:
        with app.app_context():
            db.create_all()
        print("База данных успешно инициализирована")
    except Exception as e:
        print(f"Ошибка инициализации БД: {str(e)}")

@app.cli.command("add-sample-data")
def add_sample_data():
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
