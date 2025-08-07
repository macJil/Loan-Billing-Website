import os
from datetime import datetime

class Config:
    """Configuration class for the Loan Billing System"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # MySQL Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'loan_billing_db'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    
    # Application Configuration
    APP_NAME = 'Loan Billing System'
    APP_VERSION = '1.0.0'
    APP_AUTHOR = 'Your Name'
    APP_DESCRIPTION = 'A modern loan billing and management system'
    
    # Server Configuration
    HOST = os.environ.get('HOST') or '0.0.0.0'
    PORT = int(os.environ.get('PORT') or 8080)
    
    # Database Configuration
    DB_INIT_SCRIPT = """
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
    );
    
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_username (username),
        INDEX idx_email (email)
    );
    """
    
    # Sample Data for Testing
    SAMPLE_LOANS = [
        {
            'name': 'John Smith',
            'description': 'Personal loan for home renovation',
            'date': '2024-01-15',
            'amount': 5000.00,
            'status': 'Unpaid'
        },
        {
            'name': 'Sarah Johnson',
            'description': 'Business loan for equipment purchase',
            'date': '2024-01-20',
            'amount': 15000.00,
            'status': 'Paid'
        },
        {
            'name': 'Mike Davis',
            'description': 'Emergency medical loan',
            'date': '2024-02-01',
            'amount': 3000.00,
            'status': 'Unpaid'
        }
    ]
    
    @staticmethod
    def get_mysql_config():
        """Get MySQL configuration as dictionary"""
        return {
            'MYSQL_HOST': Config.MYSQL_HOST,
            'MYSQL_USER': Config.MYSQL_USER,
            'MYSQL_PASSWORD': Config.MYSQL_PASSWORD,
            'MYSQL_DB': Config.MYSQL_DB,
            'MYSQL_PORT': Config.MYSQL_PORT
        }
    
    @staticmethod
    def validate_config():
        """Validate configuration settings"""
        errors = []
        
        if not Config.SECRET_KEY or Config.SECRET_KEY == 'your-secret-key-change-in-production':
            errors.append("Warning: Using default secret key. Change in production.")
        
        if not Config.MYSQL_HOST:
            errors.append("MYSQL_HOST is required")
        
        if not Config.MYSQL_USER:
            errors.append("MYSQL_USER is required")
        
        if not Config.MYSQL_DB:
            errors.append("MYSQL_DB is required")
        
        return errors
    
    @staticmethod
    def print_config():
        """Print current configuration (without sensitive data)"""
        print("=== Loan Billing System Configuration ===")
        print(f"App Name: {Config.APP_NAME}")
        print(f"Version: {Config.APP_VERSION}")
        print(f"Debug Mode: {Config.DEBUG}")
        print(f"Host: {Config.HOST}")
        print(f"Port: {Config.PORT}")
        print(f"MySQL Host: {Config.MYSQL_HOST}")
        print(f"MySQL Database: {Config.MYSQL_DB}")
        print(f"MySQL User: {Config.MYSQL_USER}")
        print("========================================")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'loan_billing_db_dev'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        """Initialize production-specific settings"""
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MYSQL_DB = 'loan_billing_db_test'
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 