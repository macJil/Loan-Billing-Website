from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # Change to your MySQL host
app.config['MYSQL_USER'] = 'root'       # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'mac'       # Change to your MySQL password
app.config['MYSQL_DB'] = 'loan_billing_db'  # Change to your database name

mysql = MySQL(app)

# Initialize database tables
def init_db():
    cursor = mysql.connection.cursor()
    
    # Create loans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(10) DEFAULT 'Unpaid',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """)
    
    # Create users table for future authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    mysql.connection.commit()

# Home page: list all loans
@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM loans ORDER BY created_at DESC")
        loans = cursor.fetchall()
        
        # Calculate summary statistics
        total_loans = len(loans)
        paid_loans = len([loan for loan in loans if loan['status'] == 'Paid'])
        unpaid_loans = total_loans - paid_loans
        total_amount = sum(float(loan['amount']) for loan in loans)
        paid_amount = sum(float(loan['amount']) for loan in loans if loan['status'] == 'Paid')
        unpaid_amount = total_amount - paid_amount
        
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
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        status = request.form['status']
        
        if not name or not amount:
            flash('Name and amount are required!', 'error')
            return redirect('/')
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO loans (name, description, date, amount, status) 
            VALUES (%s, %s, %s, %s, %s)
        """, (name, description, date, amount, status))
        mysql.connection.commit()
        
        flash('Loan added successfully!', 'success')
        return redirect('/')
    except Exception as e:
        flash(f'Error adding loan: {str(e)}', 'error')
        return redirect('/')

# Mark loan as paid
@app.route('/mark_paid/<int:id>')
def mark_paid(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE loans SET status='Paid' WHERE id=%s", (id,))
        mysql.connection.commit()
        flash('Loan marked as paid!', 'success')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    return redirect('/')

# Mark loan as unpaid
@app.route('/mark_unpaid/<int:id>')
def mark_unpaid(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE loans SET status='Unpaid' WHERE id=%s", (id,))
        mysql.connection.commit()
        flash('Loan marked as unpaid!', 'success')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    return redirect('/')

# Delete loan
@app.route('/delete/<int:id>')
def delete_loan(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM loans WHERE id=%s", (id,))
        mysql.connection.commit()
        flash('Loan deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting loan: {str(e)}', 'error')
    return redirect('/')

# Edit loan page
@app.route('/edit/<int:id>')
def edit_loan(id):
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM loans WHERE id=%s", (id,))
        loan = cursor.fetchone()
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
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE loans SET name=%s, description=%s, date=%s, amount=%s, status=%s 
            WHERE id=%s
        """, (name, description, date, amount, status, id))
        mysql.connection.commit()
        
        flash('Loan updated successfully!', 'success')
        return redirect('/')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
        return redirect(f'/edit/{id}')

# Search loans
@app.route('/search')
def search_loans():
    query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if query and status_filter:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE (name LIKE %s OR description LIKE %s) AND status = %s 
                ORDER BY created_at DESC
            """, (f'%{query}%', f'%{query}%', status_filter))
        elif query:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE name LIKE %s OR description LIKE %s 
                ORDER BY created_at DESC
            """, (f'%{query}%', f'%{query}%'))
        elif status_filter:
            cursor.execute("""
                SELECT * FROM loans 
                WHERE status = %s 
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
        flash(f'Search error: {str(e)}', 'error')
        return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=8080, debug=True) 