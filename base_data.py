import sqlite3
from datetime import date, datetime

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect("habits.db")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            created_date DATE DEFAULT CURRENT_DATE
        );

        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            completed BOOLEAN DEFAULT 0,
            streak_count INTEGER DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        )
                       ''')
        
        self.conn.commit()

    def insert_habit(self, text):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO habits (habit_name) VALUES (?)''', (text,))
        self.conn.commit()

    def count_habits(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM habits")
        result = cursor.fetchone()
        
        return result[0] if result else 0
    
    def count_active(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM habit_logs WHERE date=?''', (date.today(),))
        result = cursor.fetchone()
        
        return result[0] if result else 0
    
    def state_habit(self, text):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM habit_logs WHERE date=? AND habit_id = (SELECT id FROM habits WHERE habit_name =?)''', (date.today(), text,))
        result = cursor.fetchone()

        return result[0] > 0 if result else False

    def get_today_completed_status(self, habit_name):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT completed FROM habit_logs 
            WHERE habit_id = (SELECT id FROM habits WHERE habit_name = ?) 
            AND date = ?
            ORDER BY id DESC LIMIT 1
        ''', (habit_name, date.today()))
        result = cursor.fetchone()
        return result[0] if result else None

    def text_habits(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT habit_name FROM habits ORDER BY id''')
        text = cursor.fetchall()

        return [text[0][0], text[1][0], text[2][0]]
    
    def add_habit_log(self, text, type):
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO habit_logs (habit_id, completed, streak_count)
            VALUES (
                (SELECT id FROM habits WHERE habit_name = ?),
                ?,
                CASE 
                    WHEN ? = 1
                       THEN COALESCE((SELECT streak_count FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE habit_name = ?) ORDER BY id DESC LIMIT 1), 0) + 1
                    ELSE 0
                END
            )
        ''', (text, type, type, text))

        self.conn.commit()

    def get_procent_completed(self, text):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN (SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE habit_name = ?)) > 0
                    THEN ROUND(
                        (SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE habit_name = ?) AND completed = 1) * 100.0 /
                        (SELECT COUNT(*) FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE habit_name = ?))
                    , 0)
                    ELSE 0
                END
        ''', (text, text, text))
        result = cursor.fetchone()
        
        return result[0] if result else 0

    def strik(self, text):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT
                CASE
                    WHEN (COUNT(streak_count)) > 0
                        THEN streak_count
                    ELSE 0
            END
            FROM habit_logs WHERE date=? AND habit_id = (SELECT id FROM habits WHERE habit_name=?)''', (date.today(), text,))
        result = cursor.fetchone()
        
        return result[0] if result else 0

    def max_strik(self, text):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                CASE
                    WHEN COUNT(streak_count) > 0
                       THEN MAX(streak_count)
                    ELSE 0
                END
            FROM habit_logs WHERE habit_id = (SELECT id FROM habits WHERE habit_name=?)''', (text,))
        result = cursor.fetchone()
        
        return result[0] if result else 0
    
    def exmntn_21(self):
        cursor_examination = self.conn.cursor()
        cursor_examination.execute('''SELECT created_date FROM habits''')
        first_day = cursor_examination.fetchone()[0]

        date1 = date.today()
        date2 = datetime.strptime(first_day, '%Y-%m-%d').date()

        if (date1 - date2).days >= 21:
            cursor_examination.close()
            return True
        else:
            return False

    def delete_21(self):
        cursor_delete = self.conn.cursor()
        cursor_delete.execute('''DELETE FROM habit_logs''')
        cursor_delete.execute('''DELETE FROM habits''')
        cursor_delete.execute('''DELETE FROM sqlite_sequence WHERE name IN ('habits', 'habit_logs')''')
        self.conn.commit()
