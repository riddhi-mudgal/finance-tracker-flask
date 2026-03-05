import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "riddhi@8",
        database = "finance_tracker"
)

def insert_expense(date, item, category,amount, payment_mode, notes):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO expenses
    (expense_date, item_name, category, amount, payment_mode, notes)
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query,(date, item, category, amount, payment_mode, notes))
    conn.commit()   #Saves data, without this data is lost
    cursor.close()
    conn.close()

def get_all_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return expenses

def get_expenses_by_category(category):
    conn=get_db_connection()
    cursor=conn.cursor()

    query = "SELECT * FROM expenses WHERE category= %s"
    cursor.execute(query,(category,))
    expenses = cursor.fetchall()

    #Prevent memory leaks
    cursor.close()
    conn.close()

    return expenses

def get_total_expense():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total if total else 0

def get_category_totals():
    conn= get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()
    
    return data

def delete_expense(expense_id):
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("DELETE FROM expenses where id =%s", (expense_id,))
    conn.commit()

    cursor.close()
    conn.close()

def get_expense_by_id(expense_id):
    conn=get_db_connection()
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE id =%s", (expense_id,))
    expense=cursor.fetchone()

    cursor.close()
    conn.close()

    return expense

def update_expense(expense_id,item,category,amount):
    conn=get_db_connection()
    cursor=conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET item_name = %s, category=%s, amount=%s
        WHERE id= %s""",
        (item,category,amount,expense_id))
    
    conn.commit()
    cursor.close()
    conn.close()