import customtkinter as ctk

from config import VERSION


class TimeTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.defaultFont = ctk.CTkFont(family='JetBrains Mono', size=13)

        self.title(f'Трекер времени {VERSION} - Главное окно')
        self.geometry('500x400')
