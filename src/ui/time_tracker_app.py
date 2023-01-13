import customtkinter as ctk
from typing import TypeVar, Optional, Type
from datetime import datetime

from config import VERSION
from db import WorkSession, SessionBreak
from utils import filter_dict_keys


T = TypeVar('T')
def make_get_or_create_ui(master: ctk.CTk | ctk.CTkToplevel | ctk.CTkFrame, font: Optional[ctk.CTkFont] = None):
    def get_or_create_ui(name: str, entity: Type[T], *args, **kwargs) -> T:
        if not name: return None
        ui_objects = getattr(master, '__ui_objects', {}) # Получаем словать сущностей
        if ui_objects.get(name): return ui_objects.get(name) # Если сущность уже существует возвращаем еёц
        if not entity: return None
        obj = entity(master, *args, **filter_dict_keys(kwargs, ('font',)), font=kwargs.get('font', font))
        ui_objects[name] = obj # Сохраняем новую сущность в словарь
        setattr(master, '__ui_objects', ui_objects) # Сохраняем обновлённый словарь сущностей
        return obj

    return get_or_create_ui


class TimeTrackerApp(ctk.CTk):
    def __on_session_btn_click(self):
        current_date = datetime.now()
        session = WorkSession.get_last_not_finished()
        if session:
            session.session_id = session.session_id
            session.end_date = current_date
        else:
            session = WorkSession(start_date = current_date)
        session.save()
        self.draw()

    def __on_break_btn_click(self):
        session = WorkSession.get_last_not_finished()
        if not session: return
        current_date = datetime.now()
        break_obj = SessionBreak.get_last_not_finished(session.session_id)
        if break_obj:
            break_obj.break_id = break_obj.break_id
            break_obj.end_date = current_date
        else:
            break_obj = SessionBreak(session_id=session.session_id, start_date=current_date)
        break_obj.save()
        self.draw()

    def draw(self):
        get_or_create_ui = make_get_or_create_ui(self, self.defaultFont)
        session_btn = get_or_create_ui('session_btn', ctk.CTkButton, text='Начать смену', command=self.__on_session_btn_click)
        break_btn = get_or_create_ui('break_btn', ctk.CTkButton, text='Начать перерыв', command=self.__on_break_btn_click)
        session_start = get_or_create_ui('session_start', ctk.CTkLabel, text='---')
        break_start = get_or_create_ui('break_start', ctk.CTkLabel, text='---')

        session = WorkSession.get_last_not_finished()

        session_btn.configure(text=f"{'Закончи' if session else 'Нача'}ть смену")
        session_start.configure(text=str(session.start_date) if session else '---')
        if session:
            last_break = SessionBreak.get_last_not_finished(session.session_id)
            break_btn.configure(text=f"{'Закончи' if last_break else 'Нача'}ть перерыв", state='normal')
            break_start.configure(text=str(last_break.start_date) if last_break else '---')
        else:
            break_btn.configure(text='Начать перерыв', state='disabled')
            break_start.configure(text='---')

        session_start.grid(row=0, column=1)
        break_start.grid(row=1, column=1)
        session_btn.grid(row=2, column=0)
        break_btn.grid(row=2, column=1, sticky=ctk.W+ctk.E, padx=10)


    def __init__(self):
        super().__init__()
        self.defaultFont = ctk.CTkFont(family='JetBrains Mono', size=13)

        self.title(f'Трекер времени {VERSION} - Главное окно')
        self.geometry('410x100')

        self.grid_columnconfigure(0, minsize=150, pad=10)
        self.grid_columnconfigure(1, minsize=250, pad=10)
        self.grid_rowconfigure(0, pad=0)
        self.grid_rowconfigure(1, pad=0)
        self.grid_rowconfigure(2, pad=10)

        label1 = ctk.CTkLabel(self, text='Начало смены:', font=self.defaultFont)
        label2 = ctk.CTkLabel(self, text='Начало перерыва:', font=self.defaultFont)

        label1.grid(row=0, column=0, sticky=ctk.W, padx=10)
        label2.grid(row=1, column=0, sticky=ctk.W, padx=10)

        self.draw()
