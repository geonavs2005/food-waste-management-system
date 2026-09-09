import sqlite3
import os
import datetime
from config import Config

try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False

def get_db_connection():
    """
    Attempts to connect to MySQL first.
    If MySQL server is not running or accessible, automatically falls back
    to SQLite to guarantee 100% working demonstration out-of-the-box.
    """
    if PYMYSQL_AVAILABLE:
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                port=Config.MYSQL_PORT,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
                connect_timeout=2
            )
            return conn, 'mysql'
        except Exception:
            pass

    if Config.USE_SQLITE_FALLBACK:
        conn = sqlite3.connect(Config.SQLITE_DB)
        conn.row_factory = sqlite3.Row
        return conn, 'sqlite'
    else:
        raise ConnectionError("Could not connect to MySQL and SQLite fallback is disabled.")

def init_db():
    """
    Initializes tables and seeds initial sample records if the database is fresh.
    """
    conn, db_type = get_db_connection()
    cursor = conn.cursor()
    
    if db_type == 'sqlite':
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'donor',
            name TEXT NOT NULL,
            donor_id INTEGER NULL,
            recipient_id INTEGER NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS donors (
            donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            organization TEXT,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS food (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_id INTEGER,
            food_name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            expiry_date DATE NOT NULL,
            location TEXT NOT NULL,
            status TEXT DEFAULT 'Available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS recipients (
            recipient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            organization TEXT,
            contact TEXT NOT NULL,
            location TEXT NOT NULL,
            priority INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient_id INTEGER,
            food_category TEXT NOT NULL,
            quantity_requested INTEGER NOT NULL,
            priority INTEGER DEFAULT 5,
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (recipient_id) REFERENCES recipients(recipient_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT DEFAULT 'City Hub'
        );

        CREATE TABLE IF NOT EXISTS location_connections (
            connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_location TEXT NOT NULL,
            to_location TEXT NOT NULL,
            distance INTEGER DEFAULT 5
        );
        ''')
        
        # Check if donors table has records
        cursor.execute("SELECT COUNT(*) FROM donors")
        count = cursor.fetchone()[0]
        if count == 0:
            today_str = datetime.date.today().isoformat()
            tomorrow_str = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
            day2_str = (datetime.date.today() + datetime.timedelta(days=2)).isoformat()
            
            # Seed Locations
            locations_data = [
                ('Central Kitchen Hub', 'Donor Hub'),
                ('Anna Nagar Food Bank', 'Collection Center'),
                ('T Nagar Community Center', 'Collection Center'),
                ('Guindy Care Home', 'NGO/Shelter'),
                ('Velachery Relief Camp', 'NGO/Shelter'),
                ('Adyar Shelter Home', 'NGO/Shelter')
            ]
            cursor.executemany("INSERT INTO locations (name, type) VALUES (?, ?)", locations_data)
            
            # Seed Connections
            connections_data = [
                ('Central Kitchen Hub', 'Anna Nagar Food Bank', 6),
                ('Central Kitchen Hub', 'T Nagar Community Center', 8),
                ('Anna Nagar Food Bank', 'Guindy Care Home', 7),
                ('T Nagar Community Center', 'Guindy Care Home', 4),
                ('T Nagar Community Center', 'Velachery Relief Camp', 9),
                ('Guindy Care Home', 'Adyar Shelter Home', 5),
                ('Velachery Relief Camp', 'Adyar Shelter Home', 6)
            ]
            cursor.executemany("INSERT INTO location_connections (from_location, to_location, distance) VALUES (?, ?, ?)", connections_data)
            
            # Seed Donors
            donors_data = [
                ('Ramesh Kumar', '+91 98401 23456', 'Annapoorna Grand Restaurant', 'Central Kitchen Hub'),
                ('Sarah Jenkins', '+91 98402 34567', 'Green Valley Bakery', 'Anna Nagar Food Bank'),
                ('Vikram Malhotra', '+91 98403 45678', 'Taj Banquet & Events', 'T Nagar Community Center'),
                ('Priya Sunder', '+91 98404 56789', 'SRM University Cafeteria', 'Central Kitchen Hub'),
                ('Mohammed Arif', '+91 98405 67890', 'Hotel Saravana Bhavan', 'T Nagar Community Center')
            ]
            cursor.executemany("INSERT INTO donors (name, contact, organization, location) VALUES (?, ?, ?, ?)", donors_data)
            
            # Seed Food
            food_data = [
                (1, 'Vegetable Biryani', 'Meals', 45, today_str, 'Central Kitchen Hub', 'Available'),
                (2, 'Fresh Bread & Buns', 'Bread', 60, today_str, 'Anna Nagar Food Bank', 'Available'),
                (3, 'Chapati with Paneer Curry', 'Meals', 80, tomorrow_str, 'T Nagar Community Center', 'Available'),
                (1, 'Steamed Rice & Sambar', 'Meals', 50, today_str, 'Central Kitchen Hub', 'Available'),
                (4, 'Curd Rice & Pickle', 'Meals', 35, today_str, 'Central Kitchen Hub', 'Available'),
                (2, 'Mixed Fruit Baskets', 'Fruits', 25, day2_str, 'Anna Nagar Food Bank', 'Available'),
                (5, 'Idli & Sambar Packs', 'Breakfast', 40, today_str, 'T Nagar Community Center', 'Available'),
                (3, 'Dal Tadka & Jeera Rice', 'Meals', 30, tomorrow_str, 'T Nagar Community Center', 'Available'),
                (4, 'Assorted Vegetable Sandwiches', 'Snacks', 20, tomorrow_str, 'Central Kitchen Hub', 'Available'),
                (5, 'Poori & Potato Masala', 'Breakfast', 30, today_str, 'T Nagar Community Center', 'Available')
            ]
            cursor.executemany("INSERT INTO food (donor_id, food_name, category, quantity, expiry_date, location, status) VALUES (?, ?, ?, ?, ?, ?, ?)", food_data)
            
            # Seed Recipients
            recipients_data = [
                ('Father Thomas', 'St. Joseph Orphanage', '+91 98765 43210', 'Guindy Care Home', 9),
                ('Lakshmi Devi', 'Asha Old Age Home', '+91 98765 54321', 'Adyar Shelter Home', 10),
                ('Dr. Arunkumar', 'Hope Night Shelter', '+91 98765 65432', 'Velachery Relief Camp', 8),
                ('Sister Mary', 'Grace Children Foundation', '+91 98765 76543', 'Guindy Care Home', 7),
                ('Suresh Babu', 'Urban Slum Support NGO', '+91 98765 87654', 'Velachery Relief Camp', 6)
            ]
            cursor.executemany("INSERT INTO recipients (name, organization, contact, location, priority) VALUES (?, ?, ?, ?, ?)", recipients_data)
            
            # Seed Users
            users_data = [
                ('admin', 'admin123', 'admin', 'System Administrator', None, None),
                ('ramesh', 'donor123', 'donor', 'Ramesh Kumar (Annapoorna)', 1, None),
                ('sarah', 'donor123', 'donor', 'Sarah Jenkins (Green Valley)', 2, None),
                ('vikram', 'donor123', 'donor', 'Vikram Malhotra (Taj Banquet)', 3, None),
                ('thomas', 'receiver123', 'receiver', 'Father Thomas (St. Joseph Orphanage)', None, 1),
                ('lakshmi', 'receiver123', 'receiver', 'Lakshmi Devi (Asha Old Age Home)', None, 2)
            ]
            cursor.executemany("INSERT INTO users (username, password, role, name, donor_id, recipient_id) VALUES (?, ?, ?, ?, ?, ?)", users_data)

            # Seed Requests
            requests_data = [
                (2, 'Meals', 35, 10, 'Pending'),
                (1, 'Breakfast', 40, 9, 'Pending'),
                (3, 'Meals', 50, 8, 'Pending'),
                (4, 'Bread', 25, 7, 'Pending'),
                (5, 'Meals', 30, 6, 'Pending'),
                (2, 'Fruits', 20, 10, 'Pending'),
                (1, 'Snacks', 20, 9, 'Pending'),
                (3, 'Breakfast', 30, 8, 'Pending')
            ]
            cursor.executemany("INSERT INTO requests (recipient_id, food_category, quantity_requested, priority, status) VALUES (?, ?, ?, ?, ?)", requests_data)
            conn.commit()
    elif db_type == 'mysql':
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(20) NOT NULL DEFAULT 'donor',
            name VARCHAR(100) NOT NULL,
            donor_id INT NULL,
            recipient_id INT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        # Check if recipient_id column exists in MySQL users table
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN recipient_id INT NULL")
        except Exception:
            pass

        cursor.execute("SELECT COUNT(*) FROM users")
        res = cursor.fetchone()
        count = list(res.values())[0] if isinstance(res, dict) else res[0]
        if count <= 4: # Seed or update receiver accounts
            cursor.execute("""
            INSERT INTO users (username, password, role, name, donor_id, recipient_id) VALUES
            ('admin', 'admin123', 'admin', 'System Administrator', NULL, NULL),
            ('ramesh', 'donor123', 'donor', 'Ramesh Kumar (Annapoorna)', 1, NULL),
            ('sarah', 'donor123', 'donor', 'Sarah Jenkins (Green Valley)', 2, NULL),
            ('vikram', 'donor123', 'donor', 'Vikram Malhotra (Taj Banquet)', 3, NULL),
            ('thomas', 'receiver123', 'receiver', 'Father Thomas (St. Joseph Orphanage)', NULL, 1),
            ('lakshmi', 'receiver123', 'receiver', 'Lakshmi Devi (Asha Old Age Home)', NULL, 2)
            ON DUPLICATE KEY UPDATE role=VALUES(role), password=VALUES(password), recipient_id=VALUES(recipient_id);
            """)
            conn.commit()
    conn.close()

def query_db(query, args=(), one=False):
    """
    Unified query runner that handles both MySQL and SQLite seamlessly.
    Returns list of dicts or single dict.
    """
    conn, db_type = get_db_connection()
    try:
        if db_type == 'mysql':
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                rv = cursor.fetchall()
                return (rv[0] if rv else None) if one else rv
        else:
            # Replace MySQL %s parameter placeholder with SQLite ? placeholder
            sqlite_query = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            rv = [dict(row) for row in cursor.fetchall()]
            return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

def execute_db(query, args=()):
    """
    Unified query runner for INSERT, UPDATE, DELETE queries.
    Returns lastrowid.
    """
    conn, db_type = get_db_connection()
    try:
        if db_type == 'mysql':
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                conn.commit()
                return cursor.lastrowid
        else:
            sqlite_query = query.replace('%s', '?')
            cursor = conn.cursor()
            cursor.execute(sqlite_query, args)
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()
