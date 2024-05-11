select * from product
COPY Product(Brand, Name, Price, CPU, Screen, Ram, Rom) 
FROM 'D:\.CODE\.vscode\MyPythonProject\Newdata.csv' 
DELIMITER ',' 
CSV HEADER;

CREATE TABLE Customers (
    customers_id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(50)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    date DATE,
    status VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES Customers(customers_id)
);

ALTER TABLE product
ADD COLUMN product_id INT;

CREATE TABLE OrderDetails (
    order_id INT REFERENCES Orders(order_id),
    product_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY,
    product_id INT,
    quantity INT
);

UPDATE product
SET image = REPLACE(image, '//', '/')
WHERE image LIKE '%//%';

--thêm cột address vào bảng Customers
ALTER TABLE Customers
ADD COLUMN address VARCHAR(255);

INSERT INTO phone_brands (name, image_url)
--insert nhieu dong du lieu
VALUES
('Apple', 'static\brands\Apple.png'),
('Samsung', 'static\brands\Samsung.png'),
('Xiaomi', 'static\brands\Xiaomi.png'),
('Oppo', 'static\brands\Oppo.png'),
('Vivo', 'static\brands\Xiaomi.png');
('Realme', 'static\brands\Realme.png');INSERT INTO phone_brands (name, image_url)
VALUES
('Nokia', 'static/brands/Nokia.png'),
('Poco', 'static/brands/Poco.png');

--viết câu lệnh sql để thay thế cotọ image trong bảng products
UPDATE products
SET image = REPLACE(image, 'static/', 'statics/img/products/')
WHERE image LIKE '%static/%';

-- xóa bang customers
DROP TABLE customers;
-- them trường tel vào bảng customers, kiểu số điện thoại
ALTER TABLE customers
ADD COLUMN tel VARCHAR(10);

--xóa cột address trong bảng customers
ALTER TABLE customers
DROP COLUMN address;

CREATE TABLE cart (
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0),
    price NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(id) ON DELETE CASCADE
);

ALTER TABLE cart ADD PRIMARY KEY (cart_id);

-- viết câu lệnh để xóa bảng cart
DROP TABLE cart;

CREATE TABLE cart (
    cart_id SERIAL PRIMARY KEY,
    customers_id INTEGER REFERENCES Customer(id),
    product_id VARCHAR(200),
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
    price DECIMAL(10, 2)
);

--viết câu lệnh để thêm giá trị vào cột price trong bảng product ở những ô có giá trị null
UPDATE product
SET price = 0
WHERE price IS NULL;

-- đổi ỏder_id sang kiểu string
ALTER TABLE orders
ALTER COLUMN order_id TYPE VARCHAR(50);

--viết câu lệnh để them order_item_id vào bảng order_items là primary key
ALTER TABLE order_items
ADD COLUMN order_item_id SERIAL PRIMARY KEY;
-- viết đoạn code để bỏ hết primary key trong bảng order_items
ALTER TABLE order_items
DROP CONSTRAINT order_items_pkey;

--viết đoạn code xóa hết nội full trong bảng customers
DELETE FROM customers;

-- thêm trường is_staff và is_superuser vào bảng customers
ALTER TABLE customers
ADD COLUMN is_staff BOOLEAN DEFAULT FALSE,
ADD COLUMN is_superuser BOOLEAN DEFAULT FALSE;

--sửa cột is_staff và is_superuser thành true tại hàng có id bằng 16
UPDATE customers
SET is_staff = TRUE, is_superuser = TRUE
WHERE customers_id = 16;

--viết đoạn code tạo một database mới có tên là do_an_cdtt2, set up mật khẩu, cổng, 
CREATE DATABASE do_an_cdtt2;

--viết đoạn code để sap chép bảng product từ database 'CDTT2' sang "do_an_cdtt2"
CREATE TABLE do_an_cdtt2.product AS
SELECT * FROM CDTT2.product;
    
    -- cách xóa cột pin trong table product
ALTER TABLE product
DROP COLUMN pin;

-vết câu lệnh nhập dữ liệu vào table product
INSERT INTO product (brand,name,price,cpu,screen,ram,rom,product_id,image,camera,year,origin,description,os,battery)
VALUES

--sửa thuộc tính camera thành text
ALTER TABLE product
ALTER COLUMN camera TYPE TEXT;
COPY product
FROM 'D:\\.CODE\\data-1712994333627.csv'
DELIMITER ','
CSV HEADER;

--thêm trường địa chỉ cho table customers
-- viết câu lệnh để lấy tất cả thông tin của bảng order item và tên của người đặt hàng dựa theo order_id
SELECT order_items.*, customers.name
FROM order_items
JOIN orders ON order_items.order_id = orders.order_id
JOIN customers ON orders.customer_id = customers.customer_id;

ALTER TABLE product
ADD CONSTRAINT fk_product_brand
FOREIGN KEY (brand)
REFERENCES brand(name);

COPY product
FROM 'D:\\.CODE\\.vscode\\cdtt2\\Products.csv'
DELIMITER ','
CSV HEADER;

-- Sử dụng DELETE
DELETE FROM product;
DELETE FROM phone_brands;

-- Sử dụng TRUNCATE
TRUNCATE TABLE product;
TRUNCATE TABLE phone_brands;

UPDATE customer
SET password = 'new_password'
WHERE customer_id = some_id;

