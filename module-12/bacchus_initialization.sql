-- Group 5 Bacchus sql script

-- Create Bacchus database
CREATE DATABASE bacchus
    DEFAULT CHARACTER SET = 'utf8mb4';

USE bacchus

-- Create Department table
CREATE TABLE Department (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(50) NOT NULL
);

-- Create Position table
CREATE TABLE `Position` (
    position_id INT PRIMARY KEY AUTO_INCREMENT,
    position_name VARCHAR(50) NOT NULL
);

-- Create Employee table
CREATE TABLE Employee (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_first_name VARCHAR(50) NOT NULL,
    employee_last_name VARCHAR(50) NOT NULL,
    position_id INT,
    department_id INT,
    FOREIGN KEY (position_id) REFERENCES `Position`(position_id),
    FOREIGN KEY (department_id) REFERENCES Department(department_id)
);

-- Create WorkHours table
CREATE TABLE WorkHours (
    work_hours_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    work_date DATE,
    hours_worked DECIMAL(5,2),
    hourly_rate DECIMAL(6,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

-- Create Supplier table
CREATE TABLE Supplier (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_name VARCHAR(100) NOT NULL,
    supply_type VARCHAR(50)
);

-- Create Inventory table
CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100) NOT NULL,
    current_quantity INT,
    supplier_id INT,
    last_delivery_date DATE,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- Create Wine table
CREATE TABLE Wine (
    wine_id INT PRIMARY KEY AUTO_INCREMENT,
    wine_name VARCHAR(100) NOT NULL,
    wine_type VARCHAR(50),
    inventory_id INT,
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);

-- Create Distributor table
CREATE TABLE Distributor (
    distributor_id INT PRIMARY KEY AUTO_INCREMENT,
    distributor_name VARCHAR(100) NOT NULL
);

-- Create Order table
CREATE TABLE `Order` (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    distributor_id INT,
    wine_id INT,
    order_date DATE,
    shipment_date DATE,
    quantity_ordered INT,
    order_status VARCHAR(20),
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (distributor_id) REFERENCES Distributor(distributor_id),
    FOREIGN KEY (wine_id) REFERENCES Wine(wine_id)
);

-- Create Delivery table
CREATE TABLE Delivery (
    delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    tracking_number VARCHAR(50),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

-- Insert sample data

-- Department
INSERT INTO Department (department_name) VALUES 
('Finance'), ('Marketing'), ('Production'), ('Distribution'), ('Sales'), ('Technology'), ('Owner');

-- Position
INSERT INTO `Position` (position_name) VALUES 
('Finance Manager'),
('Marketing Director'),
('Administrative Assistant'),
('Production Manager'),
('Distribution Manager'),
('Sales Associate'),
('Owner');

-- Employee
INSERT INTO Employee (employee_first_name, employee_last_name, position_id, department_id) VALUES 
('Stan', 'Bacchus', 7, 7),
('David', 'Bacchus', 7, 7),
('Janet', 'Collins', 1, 1),
('Roz', 'Murphy', 2, 2),
('Bob', 'Ulrich', 2, 2),
('Henry', 'Doyle', 3, 4),
('Maria', 'Costanza', 4, 5);

-- WorkHours
INSERT INTO WorkHours (employee_id, work_date, hours_worked, hourly_rate) VALUES 
(1, '2024-09-27', 9, 40),
(2, '2024-09-27', 8.5, 40),
(3, '2024-09-27', 8, 35),
(4, '2024-09-27', 8, 35),
(5, '2024-09-27', 8, 25),
(6, '2024-09-27', 6, 35),
(7, '2024-09-27', 8, 35);

-- Supplier
INSERT INTO Supplier (supplier_name, supply_type) VALUES 
('Bottles & Corks Co', 'Bottles'),
('Bottles & Corks Co', 'Corks'),
('Shipping Supply Co', 'Boxes'),
('Shipping Supply Co', 'Labels'),
('Cook Plumbing Co', 'Vats'),
('Cook Plumbing Co', 'Tubing'),
('Bacchus Winery', 'Wine');

-- Inventory
INSERT INTO Inventory (item_name, current_quantity, supplier_id, last_delivery_date) VALUES 
('Red Wine Bottles', 1000, 1, '2024-09-20'),
('White Wine Corks', 500, 2, '2024-09-15'),
('Boxes', 5000, 3, '2024-09-25'),
('Labels', 5000, 4, '2024-09-20'),
('Vats', 100, 5, '2024-09-15'),
('Tubing', 50, 6, '2024-09-25'),
('Merlot', 75, NULL, NULL),
('Cabernet', 100, 7, NULL),
('Chablis', 150, 7, NULL),
('Chardonnay', 200, 7, NULL);

-- Wine
INSERT INTO Wine (wine_name, wine_type, inventory_id) VALUES 
('Merlot', 'Red', 7),
('Cabernet', 'Red', 8),
('Chablis', 'White', 9),
('Chardonnay', 'White', 10);

-- Distributor
INSERT INTO Distributor (distributor_name) VALUES 
('Wine World'),
('Grape Expectations'),
('Vino Ventures');

-- Order
INSERT INTO `Order` (distributor_id, wine_id, order_date, shipment_date, quantity_ordered, order_status, employee_id) VALUES 
(1, 1, '2024-09-28', '2024-10-05', 100, 'Processing', 1),
(2, 2, '2024-09-27', '2024-10-04', 75, 'Shipped', 2),
(3, 3, '2024-09-26', '2024-10-03', 50, 'Delivered', 3);

-- Delivery
INSERT INTO Delivery (supplier_id, expected_delivery_date, actual_delivery_date, tracking_number) VALUES 
(1, '2024-09-01', '2024-09-01', 'TRK123456'),
(2, '2024-09-30', '2024-09-30', 'TRK789012'),
(3, '2024-10-02', '2024-10-03', 'TRK345678'),
(4, '2024-10-01', '2024-10-01', 'TRK910112'),
(5, '2024-09-30', '2024-10-02', 'TRK131415'),
(6, '2024-10-02', NULL, 'TRK1718');