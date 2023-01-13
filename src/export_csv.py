from zipfile import ZipFile
from io import StringIO
import csv

from config import DB_PATH
from db import WorkSession, SessionBreak


break_header = ['ID смены', 'Дата начала', 'Дата окончания', 'Общая длина (мин)']
session_header = [
    'ID смены',
    'Дата начала',
    'Дата окончания',
    'Кол-во перерывов',
    'Общее время (мин)',
    'Рабочее время (мин)',
    'Время перерывов (мин)'
]


def export_to_file(path):
    session_rows = [session_header]
    break_rows = [break_header]

    sessions = WorkSession.select().order_by(WorkSession.start_date.desc()).execute()

    for session in sessions:
        total_time = None
        if session.end_date:
            total_time = (session.end_date - session.start_date).total_seconds() / 60
        total_break_time = 0
        breaks = SessionBreak.select().where(SessionBreak.session_id == session.session_id).execute()
        for break_obj in breaks:
            break_time = 0
            if break_obj.end_date:
                break_time = (break_obj.end_date - break_obj.start_date).total_seconds() / 60
            total_break_time += break_time
            break_rows.append([
                break_obj.session_id,
                break_obj.start_date.strftime('%Y-%m-%d %H:%M:%S') if break_obj.start_date else None,
                break_obj.end_date.strftime('%Y-%m-%d %H:%M:%S') if break_obj.end_date else None,
                round(break_time, 2)
            ])

        total_work_time = None
        if total_time:
            total_work_time = total_time - total_break_time

        session_rows.append([
            session.session_id,
            session.start_date.strftime('%Y-%m-%d %H:%M:%S') if session.start_date else None,
            session.end_date.strftime('%Y-%m-%d %H:%M:%S') if session.end_date else None,
            len(breaks),
            round(total_time, 2) if total_time else None,
            round(total_work_time, 2) if total_work_time else None,
            round(total_break_time, 2) if total_break_time else None
        ])

    print(session_rows)
    print(break_rows)

    if not path.endswith('.zip'):
        path = path + '.zip' 

    with ZipFile(path, 'w') as zip_data:
        zip_data.write(DB_PATH)

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerows(session_rows)
        zip_data.writestr('sessions.csv', buffer.getvalue())

        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerows(break_rows)
        zip_data.writestr('breaks.csv', buffer.getvalue())
