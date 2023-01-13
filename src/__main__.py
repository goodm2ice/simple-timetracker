from config import PROG_DIR, DB_PATH
from db import prepare_db
from ui import prepare_app


PROG_DIR.mkdir(parents=True, exist_ok=True) # Создаём директории если не существуют


def main():
    prepare_db(DB_PATH) # Инициализируем классы для работы с базой

    app = prepare_app()

    app.mainloop()


if __name__ == '__main__':
    main()
