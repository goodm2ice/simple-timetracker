from __future__ import annotations
from peewee import DatabaseProxy, SqliteDatabase, Model, AutoField, DateTimeField, ForeignKeyField
from pathlib import Path

db_proxy = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db_proxy


class WorkSession(BaseModel):
    session_id = AutoField()
    start_date = DateTimeField()
    end_date = DateTimeField(null = True)

    class Meta:
        db_table = 'WorkSessions'

    @staticmethod
    def get_last_not_finished() -> WorkSession | None:
        result = WorkSession.select().where(
                WorkSession.end_date.is_null()
            ).order_by(
                WorkSession.start_date.asc()
            ).limit(1).execute()
        if not result or len(result) <= 0:
            return None
        return result[0]


class SessionBreak(BaseModel):
    break_id = AutoField()
    session_id = ForeignKeyField(WorkSession)
    start_date = DateTimeField()
    end_date = DateTimeField(null = True)

    class Meta:
        db_table = 'SessionBreaks'
    
    @staticmethod
    def get_last_not_finished(session_id: int):
        result = SessionBreak.select().where(
                SessionBreak.session_id == session_id &
                SessionBreak.end_date.is_null()
            ).order_by(
                SessionBreak.start_date.asc()
            ).limit(1).execute()
        if not result or len(result) <= 0:
            return None
        return result[0]


def prepare_db(db_path: str) -> None:
    path = Path(db_path)
    try:
        with open(db_path, 'a'): pass # Проверка на корректность имени файла
    except OSError:
        path = path.joinpath('time_tracker_data.db') # Добавляем имя файла в конец, если его нет
    path.parent.mkdir(parents=True, exist_ok=True) # Создаём папку для базы если не существует

    db = SqliteDatabase(str(path))

    db_proxy.initialize(db)
    db.create_tables([WorkSession, SessionBreak])
