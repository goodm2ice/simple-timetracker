from pathlib import Path


VERSION = 'v0.1.0'


PROG_DIR = Path.home().joinpath('Documents/goodmice/TimeTracker')
DB_PATH = str(PROG_DIR.joinpath('time_tracker_data.db'))
