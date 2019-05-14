import sqlite3
 

class DishModel:
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dish 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER,
                             category VARCHAR(100),
                             status VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()
    
    def insert(self, title, content, user_id, category, status):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO dish 
                          (title, content, user_id) 
                          VALUES (?,?,?,?,?)''', (title, content, str(user_id), category, status))
        cursor.close()
        self.connection.commit()
    
    def get(self, dish_id ):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM dish WHERE id = ?", (str(dish_id),))
        row = cursor.fetchone()
        return row
     
    def get_all(self, user_id = None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM dish WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM dish")
        rows = cursor.fetchall()
        return rows
    
    def delete(self, dish_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM dish WHERE id = ?''', (str(dish_id)))
        cursor.close()
        self.connection.commit()