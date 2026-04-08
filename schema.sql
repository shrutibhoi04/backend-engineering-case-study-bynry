CREATE TABLE Companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Warehouses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    name VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE Products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    name VARCHAR(255),
    sku VARCHAR(100) UNIQUE,
    price DECIMAL(10,2)
);

CREATE TABLE Inventory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_id INT,
    quantity INT,
    UNIQUE(product_id, warehouse_id)
);

CREATE TABLE Suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    contact_email VARCHAR(255)
);

CREATE TABLE Product_Suppliers (
    product_id INT,
    supplier_id INT
);

CREATE TABLE Sales (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    warehouse_id INT,
    quantity_sold INT,
    sale_date TIMESTAMP
);
