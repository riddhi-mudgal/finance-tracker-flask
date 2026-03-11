import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def insert_expense(date, item, category,amount, payment_mode, notes, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO expenses
    (expense_date, item_name, category, amount, payment_mode, notes, user_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query,(date, item, category, amount, payment_mode, notes,user_id))
    conn.commit()   #Saves data, without this data is lost
    cursor.close()
    conn.close()

def get_all_expenses(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT * FROM expenses
    WHERE user_id = %s
    ORDER BY expense_date DESC
    """
    cursor.execute(query, (user_id,))
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return expenses

def get_expenses_by_category(category, user_id):
    conn=get_db_connection()
    cursor=conn.cursor()

    query = "SELECT * FROM expenses WHERE category= %s AND user_id = %s"
    cursor.execute(query,(category, user_id))
    expenses = cursor.fetchall()

    #Prevent memory leaks
    cursor.close()
    conn.close()

    return expenses

def get_total_expense(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query= """
    SELECT SUM(amount)
    FROM expenses
    WHERE user_id=%s
    """
    cursor.execute(query,(user_id,))
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total if total else 0

def get_category_totals(user_id):
    conn= get_db_connection()
    cursor = conn.cursor()

    query= """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id = %s
        GROUP BY category
    """
    cursor.execute(query,(user_id,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return data

def delete_expense(expense_id,user_id):
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM expenses where id =%s AND user_id =%s", (expense_id,user_id))
    conn.commit()

    cursor.close()
    conn.close()

def get_expense_by_id(expense_id,user_id):
    conn=get_db_connection()
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id =%s AND user_id = %s", (expense_id,user_id))
    expense=cursor.fetchone()

    cursor.close()
    conn.close()

    return expense

def update_expense(expense_id,item,category,amount,user_id):
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET item_name = %s, category=%s, amount=%s
        WHERE id= %s AND user_id=%s""",
        (item,category,amount,expense_id))
    
    conn.commit()
    cursor.close()
    conn.close()

def create_user(username, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "INSERT INTO users (username, password_hash) VALUES (%s,%s)"
    cursor.execute(query, (username,password_hash))

    conn.commit()

    cursor.close()
    conn.close()

def get_user_by_username(username):
    conn=get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query,(username,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user