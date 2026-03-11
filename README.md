# Personal Finance Tracker

A web-based Finance Tracker built using Python and Flask that helps users track their daily expenses and analyze spending patterns.

## Features
- User Authentication (Register/Login)
- Add, Edit, Delete Expenses
- Category-based Expense Tracking (Food, Travel, Shopping, Bills)
- View all expenses
- Interactive Dashboard with Charts
- Multi-user Support

## Tech Stack
Backend: Python, Flask  
Database: MySQL  
Frontend: HTML, CSS, Chart.js

## Project Structure
finance-tracker
│
├── app.py
├── db.py
├── templates
├── static

## How to Run the Project
## Setup Instructions

1. Clone the repository

git clone https://github.com/riddhi-mudgal/finance-tracker-flask.git

2. Navigate to the project folder

cd finance-tracker

3. Install dependencies

pip install -r requirements.txt

4. Create a .env file

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=finance_tracker
SECRET_KEY=your_secret_key

5. Run the application

python app.py

## Future Improvements
- Monthly reports
- Export to CSV