import sqlite3

def grant_exp(user, exp):
    db = sqlite3.connect('HiBot.db')
    cursor = db.cursor()
    cursor.execute("INSERT or IGNORE INTO main (user_id, exp, credits, messages) VALUES (?,?,?,?)", (user, exp, 0, 0))

    if cursor.rowcount == 0:
        cursor.execute(f"UPDATE main SET exp = exp + {exp} WHERE user_id = ?", (user,))
        cursor.execute(f"UPDATE main SET messages = messages + 1 WHERE user_id = ?", (user,))

    cursor.execute("SELECT * FROM main WHERE user_id = ?", (user,))
    data = cursor.fetchone()

    db.commit()
    cursor.close()

    return data
    
def grant_credits(user, credit):
    db = sqlite3.connect('HiBot.db')
    cursor = db.cursor()
    cursor.execute("INSERT or IGNORE INTO main (user_id, exp, credits, messages) VALUES (?,?,?,?)", (user, 0, credit, 0, 0))

    if cursor.rowcount == 0:
        cursor.execute(f"UPDATE main SET credits = credits + {credit} WHERE user_id = ?", (user,))

    cursor.execute("SELECT * FROM main WHERE user_id = ?", (user,))
    data = cursor.fetchone()

    db.commit()
    cursor.close()

    return data

def check_exp(user_id):
    db = sqlite3.connect('HiBot.db')
    cursor = db.cursor()
    cursor.execute("INSERT or IGNORE INTO main (user_id, exp, credits, messages) VALUES (?,?,?,?)", (user_id, 0, 0, 0))

    cursor.execute("SELECT exp FROM main WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    exp = data[0]

    db.commit()
    cursor.close()

    return exp

def check_credits(user_id):
    db = sqlite3.connect('HiBot.db')
    cursor = db.cursor()
    cursor.execute("INSERT or IGNORE INTO main (user_id, exp, credits, messagesl) VALUES (?,?,?,?)", (user_id, 0, 0, 0))

    cursor.execute("SELECT credits FROM main WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    credits = data[0]

    db.commit()
    cursor.close()

    return credits   

