# Loan Billing System

A modern, fully-featured loan billing and management system built with Flask and MySQL. Track loans, manage payments, and generate reports with a beautiful, responsive interface.

## 🚀 Features

### Core Functionality
- ✅ **Add Loans**: Create new loans with borrower name, amount, date, and description
- ✅ **View All Loans**: Comprehensive table view with sorting and filtering
- ✅ **Payment Status**: Mark loans as Paid/Unpaid with one click
- ✅ **Edit Loans**: Update loan information anytime
- ✅ **Delete Loans**: Remove loans with confirmation
- ✅ **Search & Filter**: Find loans by name, description, or status
- ✅ **Statistics Dashboard**: Real-time overview of loan portfolio

### Advanced Features
- 📊 **Real-time Statistics**: Total loans, paid/unpaid counts, and amounts
- 🔍 **Advanced Search**: Search by name, description, or filter by status
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 🎨 **Modern UI**: Beautiful Bootstrap 5 interface with custom styling
- ⌨️ **Keyboard Shortcuts**: Quick actions for power users
- 📄 **Print Reports**: Print-friendly loan reports
- 💾 **Auto-save**: Form data is automatically saved locally
- ⚡ **Fast Performance**: Optimized database queries and caching

### Technical Features
- 🗄️ **MySQL Database**: Robust data storage with proper indexing
- 🔒 **Data Validation**: Server-side and client-side validation
- 🛡️ **Error Handling**: Comprehensive error handling and user feedback
- 📈 **Scalable Architecture**: Easy to extend and maintain
- 🎯 **Accessibility**: WCAG compliant with proper focus management

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Loan-Billing-Website
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

#### Option A: Local MySQL Setup
1. Install MySQL Server
2. Create a new database:
```sql
CREATE DATABASE loan_billing_db;
CREATE USER 'loan_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON loan_billing_db.* TO 'loan_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Option B: Free MySQL Hosting (db4free.net)
1. Go to https://db4free.net
2. Register for a free account
3. Create a new database
4. Note your credentials

### Step 5: Update Database Configuration
Edit `main.py` and update the MySQL configuration:

```python
app.config['MYSQL_HOST'] = 'your-mysql-host'      # e.g., 'localhost' or 'db4free.net'
app.config['MYSQL_USER'] = 'your-username'        # e.g., 'root' or your db4free username
app.config['MYSQL_PASSWORD'] = 'your-password'    # your MySQL password
app.config['MYSQL_DB'] = 'loan_billing_db'       # your database name
```

### Step 6: Run the Application
```bash
python main.py
```

The application will be available at: `http://localhost:8080`

## 📁 Project Structure

```
Loan-Billing-Website/
├── main.py                 # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/             # HTML templates
│   ├── index.html         # Main dashboard
│   ├── edit.html          # Edit loan page
│   └── search.html        # Search and filter page
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── script.js     # JavaScript functionality
```

## 🎯 Usage Guide

### Adding a New Loan
1. Navigate to the home page
2. Fill in the loan form:
   - **Borrower Name** (required)
   - **Amount** (required)
   - **Loan Date** (required)
   - **Status** (Paid/Unpaid)
   - **Description** (optional)
3. Click "Add Loan"

### Managing Loans
- **Mark as Paid**: Click the green checkmark button
- **Mark as Unpaid**: Click the yellow undo button
- **Edit**: Click the blue edit button
- **Delete**: Click the red trash button (with confirmation)

### Searching Loans
1. Click "Search" in the navigation
2. Enter search terms in the search box
3. Optionally filter by status
4. Results update automatically

### Keyboard Shortcuts
- `Ctrl/Cmd + N`: Focus on new loan form
- `Ctrl/Cmd + F`: Focus on search box
- `Escape`: Clear search

## 🗄️ Database Schema

### Loans Table
```sql
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) DEFAULT 'Unpaid',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Users Table (for future authentication)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration Options

### Environment Variables
You can set these environment variables for configuration:

```bash
export FLASK_ENV=development
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DB=loan_billing_db
```

### Customization
- **Port**: Change port in `main.py` (default: 8080)
- **Secret Key**: Update `app.secret_key` for production
- **Database**: Modify MySQL configuration as needed

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up a reverse proxy (Nginx, Apache)
3. Configure environment variables
4. Set up SSL certificates

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "main.py"]
```

## 🧪 Testing

### Manual Testing
1. Add a test loan
2. Verify statistics update
3. Test search functionality
4. Test edit and delete operations
5. Test responsive design on mobile

### Automated Testing (Future Enhancement)
```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## 🔒 Security Considerations

- ✅ Input validation and sanitization
- ✅ SQL injection prevention with parameterized queries
- ✅ CSRF protection (Flask-WTF recommended for production)
- ✅ XSS prevention with proper escaping
- ✅ Secure headers (add Flask-Talisman for production)

## 📈 Performance Optimization

- ✅ Database indexing on frequently queried columns
- ✅ Efficient SQL queries with proper joins
- ✅ Client-side caching for static assets
- ✅ Responsive images and lazy loading
- ✅ Minified CSS and JavaScript for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
- Verify MySQL is running
- Check database credentials
- Ensure database exists

**Import Error for mysqlclient**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# On macOS
brew install mysql-connector-c

# On Windows
pip install mysqlclient --only-binary=all
```

**Port Already in Use**
- Change port in `main.py`
- Or kill the process using the port

### Getting Help
- Check the console for error messages
- Verify all dependencies are installed
- Ensure MySQL server is running
- Check database permissions

## 🎉 Features Roadmap

### Planned Enhancements
- [ ] User authentication and authorization
- [ ] Email notifications for due payments
- [ ] PDF invoice generation
- [ ] Advanced reporting and analytics
- [ ] API endpoints for mobile apps
- [ ] Multi-currency support
- [ ] Payment reminders
- [ ] Data import/export (CSV, Excel)
- [ ] Audit trail and logging
- [ ] Backup and restore functionality

### Recent Updates
- ✅ Modern Bootstrap 5 UI
- ✅ Responsive design
- ✅ Advanced search functionality
- ✅ Real-time statistics
- ✅ Keyboard shortcuts
- ✅ Auto-save form data

---

**Built with ❤️ using Flask & MySQL**

For support or questions, please open an issue on GitHub.

## 🚀 Deploying Online for Free (Render.com)

You can deploy this Flask app for free using [Render](https://render.com/):

1. **Push your code to GitHub** (if not already).
2. **Sign up at [Render](https://render.com/)** and click 'New Web Service'.
3. **Connect your GitHub repo** and select this project.
4. **Set the configuration:**
   - **Root Directory**: Leave empty (delete any value if present)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
5. **Click 'Create Web Service'** and wait for deployment.
6. **Access your app via the public URL Render provides!**

### Notes
- ✅ **SQLite Database**: The app now uses SQLite instead of MySQL, making deployment much easier.
- ✅ **Philippine Peso**: All currency is displayed in PHP (₱) format.
- ✅ **No Authentication**: The app is ready for public use without login requirements.
- ✅ **Dynamic Features**: Full CRUD operations (Create, Read, Update, Delete) for loans.
- ✅ **Free Hosting**: Render provides free hosting for small applications.

### Database
- The app automatically creates a `loan_billing.db` SQLite file when first run.
- No external database setup required - everything is self-contained.

### If you need to update the app:
- Just push changes to GitHub and Render will automatically redeploy.