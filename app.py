from flask import Flask, render_template, request, redirect, url_for, session #render_template means Flask looks into templates
from db import insert_expense, get_all_expenses, get_expenses_by_category, get_total_expense, get_category_totals, delete_expense, get_expense_by_id, update_expense, create_user, get_user_by_username
from werkzeug.security import generate_password_hash, check_password_hash
import json, csv, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)       #app is your web app, __name__ tells Flask where this file is running from it is mandatory
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")     #Decorator-adds behaviour to a function, "/" means Home page, Root URL
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")

@app.route("/add", methods=["GET","POST"])
def add_expense():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        date = request.form["date"]
        item = request.form["item"]
        category =request.form["category"]
        amount =request.form["amount"]
        payment =request.form["payment"]
        notes =request.form["notes"]

        insert_expense(date, item, category,amount, payment, notes,session['user_id'])

        return redirect(url_for("view_expenses"))
    
    return render_template("add_expense.html")

@app.route("/view")
def view_expenses():

    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user_id = session["user_id"]

    category = request.args.get("category")
    
    if category:
        expenses = get_expenses_by_category(category,session["user_id"])
    else:
        expenses = get_all_expenses(session["user_id"])

    total = get_total_expense(session["user_id"])
    category_totals = get_category_totals(session["user_id"])
    total_transactions = len(expenses)
    total_categories = len(category_totals)

    labels = [c for c, a in category_totals]
    values = [float(a) for c, a in category_totals]
    
    return render_template(
        "view_expenses.html",
        expenses = expenses,
        total=total,
        category_totals = category_totals,
        labels = json.dumps(labels),
        values = json.dumps(values),
        total_transactions = total_transactions,
        total_categories = total_categories
        )    

@app.route("/delete/<int:expense_id>")
def delete(expense_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    delete_expense(expense_id,session["user_id"])
    return redirect(url_for("view_expenses"))

@app.route("/edit/<int:expense_id>", methods=["GET","POST"])
def edit_expense(expense_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        item = request.form["item"]
        category = request.form["category"]
        amount = request.form["amount"]

        update_expense(expense_id, item, category, amount,session["user_id"])
        return redirect(url_for("view_expenses"))
    
    expense = get_expense_by_id(expense_id,session["user_id"])
    return render_template("edit_expense.html", expense=expense)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="POST":

        username=request.form["username"]
        password=request.form["password"]
        
        existing_user = get_user_by_username(username)

        if existing_user:
            return "Username already exists"

        password_hash = generate_password_hash(password)
        
        create_user(username,password_hash)

        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user and check_password_hash(user[2],password):
            session ["user_id"] = user[0]

            return redirect(url_for("home"))
        return "Invalid username or password"
    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect(url_for("login"))

@app.route("/export")
def export_csv():
    if "user_id" not in session:
        return redirect(url_for("login"))

    expenses = get_all_expenses(session["user_id"])

    from flask import Response

    def generate():
        yield "Date,Item,Category,Amount\n"
        for e in expenses:
            yield f"{e[1]},{e[2]},{e[3]},{e[4]}\n"

    return Response(generate(), mimetype="text/csv")
               
if __name__ == "__main__":      #It means Run the below code ONLY if this file is executed directly
    app.run(debug = True)       #Starts Flask web server, debug=True:- Auto reload on code change and Shows error messages in browser


