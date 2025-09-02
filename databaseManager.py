import sqlite3


class DataManager:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

        self.initialization()
        self.display_all_data()

    def initialization(self):
        with self.conn:
            self.cursor.execute(
                """CREATE TABLE IF NOT EXISTS absences (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                std_class INTEGER NOT NULL,
                                std_no INTEGER NOT NULL,
                                name TEXT NOT NULL,
                                start_date TEXT NOT NULL,
                                end_date TEXT NOT NULL,
                                abs_type TEXT NOT NULL,
                                reason TEXT)"""
            )

    def remove_absence_info(self, info):
        with self.conn:
            self.cursor.execute("DELETE from absences WHERE id=?", (info.id,))

    def display_all_data(self):
        with self.conn:
            self.cursor.execute("""SELECT * FROM absences""")

    def insert_absence_info(self, info):
        with self.conn:
            self.cursor.execute(
                "INSERT INTO absences (std_class, std_no, name, start_date, end_date, abs_type, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    info.std_class,
                    info.std_no,
                    info.name,
                    info.start_date,
                    info.end_date,
                    info.absence_abs_type,
                    info.reason,
                ),
            )
