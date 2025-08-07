#!/usr/bin/env python3
"""
Setup script for Loan Billing System
This script helps you configure and run the application
"""

import os
import sys
import subprocess
import getpass
from config import Config

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚀 Loan Billing System Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("Please run: pip install -r requirements.txt")
        sys.exit(1)

def get_mysql_config():
    """Get MySQL configuration from user"""
    print("\n🗄️  MySQL Database Configuration")
    print("-" * 40)
    
    config = {}
    
    # Host
    default_host = os.environ.get('MYSQL_HOST', 'localhost')
    host = input(f"MySQL Host [{default_host}]: ").strip() or default_host
    config['MYSQL_HOST'] = host
    
    # Port
    default_port = os.environ.get('MYSQL_PORT', '3306')
    port = input(f"MySQL Port [{default_port}]: ").strip() or default_port
    config['MYSQL_PORT'] = port
    
    # Database name
    default_db = os.environ.get('MYSQL_DB', 'loan_billing_db')
    db_name = input(f"Database Name [{default_db}]: ").strip() or default_db
    config['MYSQL_DB'] = db_name
    
    # Username
    default_user = os.environ.get('MYSQL_USER', 'root')
    user = input(f"MySQL Username [{default_user}]: ").strip() or default_user
    config['MYSQL_USER'] = user
    
    # Password
    password = getpass.getpass("MySQL Password: ")
    config['MYSQL_PASSWORD'] = password
    
    return config

def test_mysql_connection(config):
    """Test MySQL connection"""
    print("\n🔍 Testing MySQL connection...")
    
    try:
        import MySQLdb
        conn = MySQLdb.connect(
            host=config['MYSQL_HOST'],
            port=int(config['MYSQL_PORT']),
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD']
        )
        conn.close()
        print("✅ MySQL connection successful")
        return True
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        return False

def create_database(config):
    """Create database if it doesn't exist"""
    print("\n🗄️  Creating database...")
    
    try:
        import MySQLdb
        
        # First, create the database
        conn = MySQLdb.connect(
            host=config['MYSQL_HOST'],
            port=int(config['MYSQL_PORT']),
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD']
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config['MYSQL_DB']}`")
        print(f"✅ Database '{config['MYSQL_DB']}' created/verified")
        conn.commit()
        conn.close()
        
        # Now connect to the specific database and create tables
        conn = MySQLdb.connect(
            host=config['MYSQL_HOST'],
            port=int(config['MYSQL_PORT']),
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DB']
        )
        cursor = conn.cursor()
        
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_status (status),
                INDEX idx_date (date),
                INDEX idx_created_at (created_at)
            )
        """)
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_username (username),
                INDEX idx_email (email)
            )
        """)
        
        print("✅ Database tables created")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def update_main_py(config):
    """Update main.py with MySQL configuration"""
    print("\n📝 Updating main.py configuration...")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Update MySQL configuration
        content = content.replace(
            "app.config['MYSQL_HOST'] = 'localhost'",
            f"app.config['MYSQL_HOST'] = '{config['MYSQL_HOST']}'"
        )
        content = content.replace(
            "app.config['MYSQL_USER'] = 'root'",
            f"app.config['MYSQL_USER'] = '{config['MYSQL_USER']}'"
        )
        content = content.replace(
            "app.config['MYSQL_PASSWORD'] = ''",
            f"app.config['MYSQL_PASSWORD'] = '{config['MYSQL_PASSWORD']}'"
        )
        content = content.replace(
            "app.config['MYSQL_DB'] = 'loan_billing_db'",
            f"app.config['MYSQL_DB'] = '{config['MYSQL_DB']}'"
        )
        
        with open('main.py', 'w') as f:
            f.write(content)
        
        print("✅ main.py updated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to update main.py: {e}")
        return False

def create_env_file(config):
    """Create .env file for environment variables"""
    print("\n📄 Creating .env file...")
    
    env_content = f"""# Loan Billing System Environment Variables
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production

# MySQL Configuration
MYSQL_HOST={config['MYSQL_HOST']}
MYSQL_PORT={config['MYSQL_PORT']}
MYSQL_USER={config['MYSQL_USER']}
MYSQL_PASSWORD={config['MYSQL_PASSWORD']}
MYSQL_DB={config['MYSQL_DB']}

# Server Configuration
HOST=0.0.0.0
PORT=8080
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def add_sample_data(config):
    """Add sample data to the database"""
    print("\n📊 Adding sample data...")
    
    try:
        import MySQLdb
        conn = MySQLdb.connect(
            host=config['MYSQL_HOST'],
            port=int(config['MYSQL_PORT']),
            user=config['MYSQL_USER'],
            password=config['MYSQL_PASSWORD'],
            database=config['MYSQL_DB']
        )
        cursor = conn.cursor()
        
        # Check if sample data already exists
        cursor.execute("SELECT COUNT(*) FROM loans")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert sample data
            for loan in Config.SAMPLE_LOANS:
                cursor.execute("""
                    INSERT INTO loans (name, description, date, amount, status)
                    VALUES (%s, %s, %s, %s, %s)
                """, (loan['name'], loan['description'], loan['date'], loan['amount'], loan['status']))
            
            conn.commit()
            print("✅ Sample data added successfully")
        else:
            print("ℹ️  Sample data already exists, skipping...")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to add sample data: {e}")
        return False

def run_application():
    """Run the Flask application"""
    print("\n🚀 Starting Loan Billing System...")
    print("=" * 60)
    print("📱 Application will be available at: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Get MySQL configuration
    mysql_config = get_mysql_config()
    
    # Test MySQL connection
    if not test_mysql_connection(mysql_config):
        print("\n❌ Please check your MySQL configuration and try again")
        return
    
    # Create database and tables
    if not create_database(mysql_config):
        print("\n❌ Database setup failed")
        return
    
    # Update main.py
    if not update_main_py(mysql_config):
        print("\n❌ Configuration update failed")
        return
    
    # Create .env file
    create_env_file(mysql_config)
    
    # Add sample data
    add_sample_data(mysql_config)
    
    print("\n✅ Setup completed successfully!")
    print("\n🎉 Your Loan Billing System is ready to use!")
    
    # Ask if user wants to run the application
    run_now = input("\n🚀 Would you like to start the application now? (y/n): ").lower().strip()
    if run_now in ['y', 'yes']:
        run_application()
    else:
        print("\n📝 To run the application later, use:")
        print("   python main.py")
        print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 