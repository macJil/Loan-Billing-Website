from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import os
from github_db import github_db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Home page: list all loans
@app.route('/')
def index():
    try:
        loans = github_db.get_all_loans()
        
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
        print("[DEBUG] Received POST to /add")
        print(f"[DEBUG] Raw amount from form: {request.form['amount']}")
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        amount = float(request.form['amount'])
        status = request.form['status']
        print(f"[DEBUG] Form data: name={name}, amount={amount}, date={date}, status={status}")

        if not name or not amount:
            flash('Name and amount are required!', 'error')
            print("[DEBUG] Validation failed: missing name or amount")
            return redirect('/')
        
        loan_data = {
            'name': name,
            'description': description,
            'date': date,
            'amount': amount,
            'status': status
        }
        
        success, new_id = github_db.add_loan(loan_data)
        
        if success:
            print("[DEBUG] Loan added successfully")
            flash('Loan added successfully!', 'success')
        else:
            print("[DEBUG] Failed to add loan")
            flash('Failed to add loan. Please try again.', 'error')
        
        return redirect('/')
    except Exception as e:
        print(f"[DEBUG] Error adding loan: {e}")
        flash(f'Error adding loan: {str(e)}', 'error')
        return redirect('/')

# Mark loan as paid
@app.route('/mark_paid/<int:id>')
def mark_paid(id):
    try:
        loan = github_db.get_loan_by_id(id)
        if loan:
            loan['status'] = 'Paid'
            success = github_db.update_loan(id, loan)
            if success:
                flash('Loan marked as paid!', 'success')
            else:
                flash('Failed to update loan.', 'error')
        else:
            flash('Loan not found!', 'error')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    
    return redirect('/')

# Mark loan as unpaid
@app.route('/mark_unpaid/<int:id>')
def mark_unpaid(id):
    try:
        loan = github_db.get_loan_by_id(id)
        if loan:
            loan['status'] = 'Unpaid'
            success = github_db.update_loan(id, loan)
            if success:
                flash('Loan marked as unpaid!', 'success')
            else:
                flash('Failed to update loan.', 'error')
        else:
            flash('Loan not found!', 'error')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
    
    return redirect('/')

# Delete a loan
@app.route('/delete/<int:id>')
def delete_loan(id):
    try:
        success = github_db.delete_loan(id)
        if success:
            flash('Loan deleted successfully!', 'success')
        else:
            flash('Failed to delete loan.', 'error')
    except Exception as e:
        flash(f'Error deleting loan: {str(e)}', 'error')
    
    return redirect('/')

# Edit loan page
@app.route('/edit/<int:id>')
def edit_loan(id):
    try:
        loan = github_db.get_loan_by_id(id)
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
        amount = float(request.form['amount'])
        status = request.form['status']
        
        if not name or not amount:
            flash('Name and amount are required!', 'error')
            return redirect(f'/edit/{id}')
        
        loan_data = {
            'name': name,
            'description': description,
            'date': date,
            'amount': amount,
            'status': status
        }
        
        success = github_db.update_loan(id, loan_data)
        
        if success:
            flash('Loan updated successfully!', 'success')
        else:
            flash('Failed to update loan.', 'error')
        
        return redirect('/')
    except Exception as e:
        flash(f'Error updating loan: {str(e)}', 'error')
        return redirect(f'/edit/{id}')

# Search loans
@app.route('/search')
def search_loans():
    try:
        query = request.args.get('q', '')
        status_filter = request.args.get('status', '')
        
        loans = github_db.search_loans(query, status_filter)
        
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
        flash(f'Database error: {str(e)}', 'error')
        return render_template('search.html', loans=[], 
                             query='', status_filter='',
                             total_loans=0, paid_loans=0, unpaid_loans=0,
                             total_amount=0, paid_amount=0, unpaid_amount=0)

if __name__ == '__main__':
    app.run(debug=True) 