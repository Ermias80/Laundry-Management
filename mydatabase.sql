CREATE DATABASE Laundery_managemen7;
USE Laundery_managemen7;

CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'admin', 'staff') NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATE NOT NULL,
    pickup_date DATE,
    delivery_date DATE,
    status ENUM('pending', 'in_process', 'completed') DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO Service (name, description, price) VALUES
('Jacket', 'Basic washing and Ironing service.', 40.00),
('Sweater', 'Basic washing and Ironing service.', 15.00),
('Pajamas', 'Basic washing and Ironing service.', 20.00),
('Jeans', 'Basic washing and Ironing service.', 25.00),
('T-shirt', 'Basic washing and Ironing service.', 25.00),
('Dress', 'Basic washing and Ironing service.', 30.00),
('Shirt', 'Basic washing and Ironing service.', 25.00),
('Skirt', 'Basic washing and Ironing service.', 10.00),
('Coat', 'Basic washing and Ironing service.', 20.00);


CREATE TABLE Payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATE NOT NULL,
    payment_method ENUM('Telebirr', 'M-pesa', 'CBE-Birr', 'Awashbirr_pro') NOT NULL,
    status ENUM('paid', 'pending') DEFAULT 'pending',
    FOREIGN KEY (order_id) REFERENCES Orders(id) ON DELETE CASCADE
);

CREATE TABLE Notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    type ENUM('SMS', 'email') NOT NULL,
    status ENUM('sent', 'not_sent') DEFAULT 'sent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);