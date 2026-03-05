from flask import Flask, render_template, request, redirect, url_for #render_template means Flask looks into templates
from db import insert_expense, get_all_expenses, get_expenses_by_category, get_total_expense, get_category_totals, delete_expense, get_expense_by_id, update_expense
import json

app = Flask(__name__)       #app is your web app, __name__ tells Flask where this file is running from it is mandatory

@app.route("/")     #Decorator-adds behaviour to a function, "/" means Home page, Root URL
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET","POST"])
def add_expense():
    if request.method == "POST":
        date = request.form["date"]
        item = request.form["item"]
        category =request.form["category"]
        amount =request.form["amount"]
        payment =request.form["payment"]
        notes =request.form["notes"]

        insert_expense(date, item, category,amount, payment, notes)

        return redirect(url_for("view_expenses"))
    
    return render_template("add_expense.html")

@app.route("/view")
def view_expenses():
    category = request.args.get("category")
    
    if category:
        expenses = get_expenses_by_category(category)
    else:
        expenses = get_all_expenses()

    total = get_total_expense()
    category_totals = get_category_totals()
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
    delete_expense(expense_id)
    return redirect(url_for("view_expenses"))

@app.route("/edit/<int:expense_id>", methods=["GET","POST"])
def edit_expense(expense_id):
    if request.method == "POST":
        item = request.form["item"]
        category = request.form["category"]
        amount = request.form["amount"]

        update_expense(expense_id, item, category, amount)
        return redirect(url_for("view_expenses"))
    
    expense = get_expense_by_id(expense_id)
    return render_template("edit_expense.html", expense=expense)



if __name__ == "__main__":      #It means Run the below code ONLY if this file is executed directly
    app.run(debug = True)       #Starts Flask web server, debug=True:- Auto reload on code change and Shows error messages in browser


