-- ==========================================================
-- Food Waste Management System - Database Schema & Sample Data
-- Database: MySQL
-- ==========================================================

CREATE DATABASE IF NOT EXISTS food_waste_db;
USE food_waste_db;

-- 1. Users & Authentication Table (Multi-Role: Admin, Donor, Receiver)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'donor', -- 'admin', 'donor', or 'receiver'
    name VARCHAR(100) NOT NULL,
    donor_id INT NULL,       -- Linked to donor profile if role is 'donor'
    recipient_id INT NULL,   -- Linked to recipient profile if role is 'receiver'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Donors Table
CREATE TABLE IF NOT EXISTS donors (
    donor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    organization VARCHAR(150),
    location VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Food Inventory Table (Linked List storage)
CREATE TABLE IF NOT EXISTS food (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    donor_id INT,
    food_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INT NOT NULL,
    expiry_date DATE NOT NULL,
    location VARCHAR(100) NOT NULL,
    status VARCHAR(30) DEFAULT 'Available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES donors(donor_id) ON DELETE SET NULL
);

-- 4. Recipients Table
CREATE TABLE IF NOT EXISTS recipients (
    recipient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    organization VARCHAR(150),
    contact VARCHAR(20) NOT NULL,
    location VARCHAR(100) NOT NULL,
    priority INT DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Requests Table (FIFO Queue processing)
CREATE TABLE IF NOT EXISTS requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    recipient_id INT,
    food_category VARCHAR(50) NOT NULL,
    quantity_requested INT NOT NULL,
    priority INT DEFAULT 5,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (recipient_id) REFERENCES recipients(recipient_id) ON DELETE CASCADE
);

-- 6. Locations Table (Graph Vertices)
CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    type VARCHAR(50) DEFAULT 'City Hub'
);

-- 7. Location Connections Table (Graph Edges)
CREATE TABLE IF NOT EXISTS location_connections (
    connection_id INT AUTO_INCREMENT PRIMARY KEY,
    from_location VARCHAR(100) NOT NULL,
    to_location VARCHAR(100) NOT NULL,
    distance INT DEFAULT 5,
    FOREIGN KEY (from_location) REFERENCES locations(name) ON DELETE CASCADE,
    FOREIGN KEY (to_location) REFERENCES locations(name) ON DELETE CASCADE
);

-- ==========================================================
-- Insert Initial Authentication Users (Admin & Donors)
-- ==========================================================

INSERT INTO users (username, password, role, name, donor_id, recipient_id) VALUES
('admin', 'admin123', 'admin', 'System Administrator', NULL, NULL),
('ramesh', 'donor123', 'donor', 'Ramesh Kumar (Annapoorna)', 1, NULL),
('sarah', 'donor123', 'donor', 'Sarah Jenkins (Green Valley)', 2, NULL),
('vikram', 'donor123', 'donor', 'Vikram Malhotra (Taj Banquet)', 3, NULL),
('thomas', 'receiver123', 'receiver', 'Father Thomas (St. Joseph Orphanage)', NULL, 1),
('lakshmi', 'receiver123', 'receiver', 'Lakshmi Devi (Asha Old Age Home)', NULL, 2)
ON DUPLICATE KEY UPDATE role=VALUES(role), password=VALUES(password), recipient_id=VALUES(recipient_id);

-- ==========================================================
-- Insert Sample Locations
-- ==========================================================

INSERT INTO locations (name, type) VALUES
('Central Kitchen Hub', 'Donor Hub'),
('Anna Nagar Food Bank', 'Collection Center'),
('T Nagar Community Center', 'Collection Center'),
('Guindy Care Home', 'NGO/Shelter'),
('Velachery Relief Camp', 'NGO/Shelter'),
('Adyar Shelter Home', 'NGO/Shelter')
ON DUPLICATE KEY UPDATE type=VALUES(type);

INSERT INTO location_connections (from_location, to_location, distance) VALUES
('Central Kitchen Hub', 'Anna Nagar Food Bank', 6),
('Central Kitchen Hub', 'T Nagar Community Center', 8),
('Anna Nagar Food Bank', 'Guindy Care Home', 7),
('T Nagar Community Center', 'Guindy Care Home', 4),
('T Nagar Community Center', 'Velachery Relief Camp', 9),
('Guindy Care Home', 'Adyar Shelter Home', 5),
('Velachery Relief Camp', 'Adyar Shelter Home', 6)
ON DUPLICATE KEY UPDATE distance=VALUES(distance);

-- Sample Donors
INSERT INTO donors (donor_id, name, contact, organization, location) VALUES
(1, 'Ramesh Kumar', '+91 98401 23456', 'Annapoorna Grand Restaurant', 'Central Kitchen Hub'),
(2, 'Sarah Jenkins', '+91 98402 34567', 'Green Valley Bakery', 'Anna Nagar Food Bank'),
(3, 'Vikram Malhotra', '+91 98403 45678', 'Taj Banquet & Events', 'T Nagar Community Center'),
(4, 'Priya Sunder', '+91 98404 56789', 'SRM University Cafeteria', 'Central Kitchen Hub'),
(5, 'Mohammed Arif', '+91 98405 67890', 'Hotel Saravana Bhavan', 'T Nagar Community Center')
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Food Inventory
INSERT INTO food (food_id, donor_id, food_name, category, quantity, expiry_date, location, status) VALUES
(1, 1, 'Vegetable Biryani', 'Meals', 45, CURDATE(), 'Central Kitchen Hub', 'Available'),
(2, 2, 'Fresh Bread & Buns', 'Bread', 60, CURDATE(), 'Anna Nagar Food Bank', 'Available'),
(3, 3, 'Chapati with Paneer Curry', 'Meals', 80, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'T Nagar Community Center', 'Available'),
(4, 1, 'Steamed Rice & Sambar', 'Meals', 50, CURDATE(), 'Central Kitchen Hub', 'Available'),
(5, 4, 'Curd Rice & Pickle', 'Meals', 35, CURDATE(), 'Central Kitchen Hub', 'Available'),
(6, 2, 'Mixed Fruit Baskets', 'Fruits', 25, DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'Anna Nagar Food Bank', 'Available'),
(7, 5, 'Idli & Sambar Packs', 'Breakfast', 40, CURDATE(), 'T Nagar Community Center', 'Available'),
(8, 3, 'Dal Tadka & Jeera Rice', 'Meals', 30, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'T Nagar Community Center', 'Available'),
(9, 4, 'Assorted Vegetable Sandwiches', 'Snacks', 20, DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'Central Kitchen Hub', 'Available'),
(10, 5, 'Poori & Potato Masala', 'Breakfast', 30, CURDATE(), 'T Nagar Community Center', 'Available')
ON DUPLICATE KEY UPDATE food_name=VALUES(food_name);

-- Sample Recipients
INSERT INTO recipients (recipient_id, name, organization, contact, location, priority) VALUES
(1, 'Father Thomas', 'St. Joseph Orphanage', '+91 98765 43210', 'Guindy Care Home', 9),
(2, 'Lakshmi Devi', 'Asha Old Age Home', '+91 98765 54321', 'Adyar Shelter Home', 10),
(3, 'Dr. Arunkumar', 'Hope Night Shelter', '+91 98765 65432', 'Velachery Relief Camp', 8),
(4, 'Sister Mary', 'Grace Children Foundation', '+91 98765 76543', 'Guindy Care Home', 7),
(5, 'Suresh Babu', 'Urban Slum Support NGO', '+91 98765 87654', 'Velachery Relief Camp', 6)
ON DUPLICATE KEY UPDATE name=VALUES(name);

-- Sample Requests
INSERT INTO requests (request_id, recipient_id, food_category, quantity_requested, priority, request_date, status) VALUES
(1, 2, 'Meals', 35, 10, NOW() - INTERVAL 3 HOUR, 'Pending'),
(2, 1, 'Breakfast', 40, 9, NOW() - INTERVAL 2 HOUR, 'Pending'),
(3, 3, 'Meals', 50, 8, NOW() - INTERVAL 90 MINUTE, 'Pending'),
(4, 4, 'Bread', 25, 7, NOW() - INTERVAL 60 MINUTE, 'Pending'),
(5, 5, 'Meals', 30, 6, NOW() - INTERVAL 45 MINUTE, 'Pending'),
(6, 2, 'Fruits', 20, 10, NOW() - INTERVAL 30 MINUTE, 'Pending'),
(7, 1, 'Snacks', 20, 9, NOW() - INTERVAL 15 MINUTE, 'Pending'),
(8, 3, 'Breakfast', 30, 8, NOW() - INTERVAL 5 MINUTE, 'Pending')
ON DUPLICATE KEY UPDATE food_category=VALUES(food_category);
