CREATE DATABASE IF NOT EXISTS Nish_healing_center;
USE Nish_healing_center;

CREATE TABLE Healer (
    healer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    specialty VARCHAR(50),
    fee INT
);

CREATE TABLE Potion (
    potion_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    dosage VARCHAR(50),
    price INT
);

CREATE TABLE Analysis (
    analysis_id INT PRIMARY KEY AUTO_INCREMENT,
    test_name VARCHAR(50),
    details VARCHAR(100),
    cost INT
);

CREATE TABLE Supper (
    supper_id INT PRIMARY KEY AUTO_INCREMENT,
    meal_name VARCHAR(50),
    diet_type VARCHAR(50),
    price INT
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    gender VARCHAR(15),
    phone VARCHAR(15),
    days INT,
    healer_id INT,
    potion_id INT,
    analysis_id INT,
    supper_id INT,
    FOREIGN KEY (healer_id) REFERENCES Healer(healer_id),
    FOREIGN KEY (potion_id) REFERENCES Potion(potion_id),
    FOREIGN KEY (analysis_id) REFERENCES Analysis(analysis_id),
    FOREIGN KEY (supper_id) REFERENCES Supper(supper_id)
);

INSERT INTO Healer (name, specialty, fee) VALUES
('Dr. Aarav Sharma', 'General Physician', 600),
('Dr. Meera Nair', 'Cardiologist', 1200),
('Dr. Rohan Verma', 'Orthopedic', 1000),
('Dr. Kavita Joshi', 'Neurologist', 1500);

INSERT INTO Potion (name, dosage, price) VALUES
('Paracetamol 650mg', '2 times a day', 120),
('Amoxicillin 500mg', '3 times a day', 350),
('Pantoprazole 40mg', 'Before breakfast', 180),
('Atorvastatin 10mg', 'At night', 420);

INSERT INTO Analysis (test_name, details, cost) VALUES
('CBC Blood Test', 'Complete blood count', 450),
('ECG and Echo', 'Heart checkup', 1800),
('Digital X-Ray', 'Chest and bone scan', 700),
('MRI Brain Scan', 'Full brain scan', 4500);

INSERT INTO Supper (meal_name, diet_type, price) VALUES
('Moong Dal Khichdi', 'Light Diet', 250),
('Oats and Boiled Veggies', 'Low Salt Diet', 320),
('Paneer and Roti Meal', 'High Protein', 400),
('Vegetable Soup and Fruits', 'Soft Diet', 200);

INSERT INTO Customer (name, age, gender, phone, days, healer_id, potion_id, analysis_id, supper_id) VALUES
('Ananya Gupta', 24, 'Female', '9876543210', 2, 1, 1, 1, 1),
('Vikram Singh', 48, 'Male', '9826012345', 4, 2, 4, 2, 2),
('Riya Patel', 31, 'Female', '9123456789', 3, 3, 2, 3, 3);