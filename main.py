from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# SQLite Configuration
DATABASE = '/tmp/loan_billing.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Initialize database tables
def init_db():
    db = get_db()
    cursor = db.cursor()
    
    # Create loans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'Unpaid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create users table for future authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    db.commit()
    db.close()

# Home page: list all loans
@app.route('/')
def index():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM loans ORDER BY created_at DESC")
        loans = cursor.fetchall()
        
        # Calculate summary statistics
        total_loans = len(loans)
        paid_loans = len([loan for loan in loans if loan['status'] == 'Paid'])
        unpaid_loans = total_loans - paid_loans
        total_amount = sum(float(loan['amount']) for loan in loans)
        paid_amount = sum(float(loan['amount']) for loan in loans if loan['status'] == 'Paid')
        unpaid_amount = total_amount - paid_amount
        
        db.close()
        
        return render_template('index.html', 
                             loans=loans, 
                             total_loans=total_loans,
                             paid_loans=paid_loans,
                             unpaid_loans=unpaid_loans,
                             total_amount=total_amount,
                             paid_amount=paid_amount,
                             unpaid_amount=unpaid_amount)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('index.html', loans=[], 
                             total_loans=0, paid_loans=0, unpaid_loans=0,
                             total_amount=0, paid_amount=0, unpaid_amount=0)

# Add a loan
@app.route('/add', methods=['POST'])
def add_loan():
    try:
        print("[DEBUG] Received POST to /add")
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        status = request.form['status']
        print(f"[DEBUG] Form data: name={name}, amount={amount}, date={date}, status={status}")
        
        if not name or not amount:
            flash('Name and amount are required!', 'error')
            print("[DEBUG] Validation failed: missing name or amount")
            return redirect('/')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO loans (name, description, date, amount, status) 
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, date, amount, status))
        db.commit()
        db.close()
        print("[DEBUG] Loan added successfully")
        
        flash('Loan added successfully!', 'success')
        return redirect('/')
    except Exception as e:
        print(f"[DEBUG] Error adding loan: {e}")
        flash(f'Error adding loan: {str(e)}', 'error')
        return redirect('/')

# Mark loan as paid
@app.route('/mark_paid/<int:id>')
def mark_paid(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE loans SET status = 'Paid' WHERE id = ?", (id,))
        db.commit()
        db.close()
        
        flash('Loan marked as paid!', 'success')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    
    return redirect('/')

# Mark loan as unpaid
@app.route('/mark_unpaid/<int:id>')
def mark_unpaid(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE loans SET status = 'Unpaid' WHERE id = ?", (id,))
        db.commit()
        db.close()
        
        flash('Loan marked as unpaid!', 'success')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    
    return redirect('/')

# Delete a loan
@app.route('/delete/<int:id>')
def delete_loan(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM loans WHERE id = ?", (id,))
        db.commit()
        db.close()
        
        flash('Loan deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting loan: {str(e)}', 'error')
    
    return redirect('/')

# Edit loan page
@app.route('/edit/<int:id>')
def edit_loan(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM loans WHERE id = ?", (id,))
        loan = cursor.fetchone()
        db.close()
        
        if loan:
            return render_template('edit.html', loan=loan)
        else:
            flash('Loan not found!', 'error')
            return redirect('/')
    except Exception as e:
        flash(f'Error loading loan: {str(e)}', 'error')
        return redirect('/')

# Update loan
@app.route('/update/<int:id>', methods=['POST'])
def update_loan(id):
    try:
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        status = request.form['status']
        
        if not name or not amount:
            flash('Name and amount are required!', 'error')
            return redirect(f'/edit/{id}')
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE loans 
            SET name = ?, description = ?, date = ?, amount = ?, status = ?
            WHERE id = ?
        """, (name, description, date, amount, status, id))
        db.commit()
        db.close()
        
        flash('Loan updated successfully!', 'success')
        return redirect('/')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
        return redirect(f'/edit/{id}')

# Search loans
@app.route('/search')
def search_loans():
    try:
        query = request.args.get('query', '')
        status_filter = request.args.get('status', '')
        
        db = get_db()
        cursor = db.cursor()
        
        if query and status_filter:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE (name LIKE ? OR description LIKE ?) AND status = ?
                ORDER BY created_at DESC
            """, (f'%{query}%', f'%{query}%', status_filter))
        elif query:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE name LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
            """, (f'%{query}%', f'%{query}%'))
        elif status_filter:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE status = ?
                ORDER BY created_at DESC
            """, (status_filter,))
        else:
            cursor.execute("SELECT * FROM loans ORDER BY created_at DESC")
        
        loans = cursor.fetchall()
        
        # Calculate summary statistics
        total_loans = len(loans)
        paid_loans = len([loan for loan in loans if loan['status'] == 'Paid'])
        unpaid_loans = total_loans - paid_loans
        total_amount = sum(float(loan['amount']) for loan in loans)
        paid_amount = sum(float(loan['amount']) for loan in loans if loan['status'] == 'Paid')
        unpaid_amount = total_amount - paid_amount
        
        db.close()
        
        return render_template('search.html', 
                             loans=loans, 
                             query=query,
                             status_filter=status_filter,
                             total_loans=total_loans,
                             paid_loans=paid_loans,
                             unpaid_loans=unpaid_loans,
                             total_amount=total_amount,
                             paid_amount=paid_amount,
                             unpaid_amount=unpaid_amount)
    except Exception as e:
        flash(f'Database error: {str(e)}', 'error')
        return render_template('search.html', loans=[], 
                             query='', status_filter='',
                             total_loans=0, paid_loans=0, unpaid_loans=0,
                             total_amount=0, paid_amount=0, unpaid_amount=0)

if __name__ == '__main__':
    app.run(debug=True)

# Always initialize the database, even when run by Gunicorn
with app.app_context():
    init_db()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print("[DEBUG] Tables in database:", cursor.fetchall())
    db.close() 