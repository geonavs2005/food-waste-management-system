import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'food_waste_dsa_secret_key_2026')
    
    # MySQL Database Configuration
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'admin')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'food_waste_db')
    
    # Fallback to local SQLite database if MySQL server is not running
    SQLITE_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'food_waste.db')
    USE_SQLITE_FALLBACK = True
