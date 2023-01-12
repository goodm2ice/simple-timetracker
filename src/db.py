from peewee import DatabaseProxy, SqliteDatabase, Model, AutoField, DateField, ForeignKeyField
from pathlib import Path


db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class WorkSession(BaseModel):
    session_id = AutoField()
    start_date = DateField()
    end_date = DateField(null = True)

    class Meta:
        db_table = 'WorkSessions'


class SessionBreak(BaseModel):
    break_id = AutoField()
    session_id = ForeignKeyField(WorkSession)
    start_date = DateField()
    end_date = DateField(null = True)

    class Meta:
        db_table = 'SessionBreaks'
        indexes = (
            (('session_id', 'start_date'), True),
            (('session_id', 'end_date'), True),
        )


def prepare_db(db_path: str) -> None:
    path = Path(db_path)
    try:
        with open(db_path, 'a'): pass # Проверка на корректность имени файла
    except OSError:
        path = path.joinpath('time_tracker_data.db') # Добавляем имя файла в конец, если его нет
    path.parent.mkdir(parents=True, exist_ok=True) # Создаём папку для базы если не существует

    db = SqliteDatabase(str(path))

    db_proxy.initialize(db)
    db.create_tables([WorkSession])
