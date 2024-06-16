import sqlite3

def connect_users():
    return sqlite3.connect("users.db")

def users_table(db): 
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users_table (discord_id, codeforcer_name);")
    db.commit()

def store_user(db, discord_id, codeforcer_name):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM users_table WHERE discord_id = ?", (discord_id,))
    user = res.fetchone()
    cursor.close()
    if user:
        cursor = db.cursor()
        cursor.execute("UPDATE users_table Set codeforcer_name = ? WHERE discord_id = ?", (codeforcer_name, discord_id))
        db.commit()
        return False
    else:
        cursor = db.cursor()
        cursor.execute("INSERT INTO users_table VALUES(?, ?)", (discord_id, codeforcer_name))
        db.commit()
        return True

def get_user(db, discord_id):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM users_table WHERE discord_id = ?", (discord_id,))
    user = res.fetchone()
    cursor.close()

    return user[1] if user else None

def remove_user(db, discord_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM users_table WHERE discord_id = ?", (discord_id,))
    cursor.close()
    db.commit()
    
