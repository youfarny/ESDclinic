DROP DATABASE IF EXISTS patient;  
CREATE DATABASE `patient` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `patient`.`patient` (
  `patient_id` INT NOT NULL AUTO_INCREMENT,
  `patient_name` VARCHAR(100) NOT NULL,
  `patient_password` VARCHAR(100) NOT NULL,
  `patient_contact` INT NOT NULL,
  `patient_address` VARCHAR(200) NOT NULL,
  `patient_insurance` TINYINT NOT NULL,
  `patient_allergies` JSON NOT NULL,
  `patient_age` INT NOT NULL,
  PRIMARY KEY (`patient_id`),
  UNIQUE INDEX `patient_id_UNIQUE` (`patient_id` ASC) VISIBLE);
  
  -- Insert fake patients
INSERT INTO `patient`.`patient` (patient_name, patient_password, patient_contact, patient_address, patient_insurance, patient_allergies, patient_age)
VALUES 
('John Doe', 'password', 97208453, '123 Main St', 1, '["Ibuprofen"]', 13),
('Jane Smith', 'password', 97208453, '456 Oak St', 0, '["None"]', 15),
('Alice Johnson', 'password', 97208453, '789 Pine St', 1, '["Antihistamines"]', 57),
('Bob Williams', 'password', 97208453, '101 Maple St', 0, '["Paracetamol"]', 3),
('Emily Brown', 'password', 97208453, '202 Birch St', 1, '["None"]', 109);
  
DROP DATABASE IF EXISTS queue;  
CREATE DATABASE `queue` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `queue`.`queue` (
  `appointment_id` INT NOT NULL,
  `doctor_id` INT NOT NULL,
  `patient_contact` INT NOT NULL,
  PRIMARY KEY (`appointment_id`),
  UNIQUE INDEX `appointment_id_UNIQUE` (`appointment_id` ASC) VISIBLE);
  
  -- Insert fake queue
INSERT INTO `queue`.`queue` (appointment_id, doctor_id, patient_contact)
VALUES 
(2, 2, 97208453),
(3, 3, 97208453),
(4, 3, 97208453),
(5, 2, 97208453);

DROP DATABASE IF EXISTS appointment;  
CREATE DATABASE `appointment` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

CREATE TABLE `appointment`.`appointment` (
  `appointment_id` INT NOT NULL AUTO_INCREMENT,
  `patient_id` INT NOT NULL,
  `patient_symptoms` JSON NOT NULL,
  `notes` JSON NULL,
  `diagnosis` LONGTEXT NULL,
  `doctor_id` INT NULL,
  `prescription_id` INT NULL,
  `payment_id` INT NULL,
  `start_time` DATETIME NULL,
  `end_time` DATETIME NULL,
  PRIMARY KEY (`appointment_id`),
  UNIQUE INDEX `appointment_id_UNIQUE` (`appointment_id` ASC) VISIBLE
);

INSERT INTO `appointment`.`appointment` 
    (patient_id, patient_symptoms, notes, diagnosis, doctor_id, prescription_id, payment_id, start_time, end_time)
VALUES 
    (1, '["Fever", "Headache"]', '[{"diagnosis": "Influenza (Flu)", "confidence": 90}, {"diagnosis": "Common Cold", "confidence": 85}]', 'Viral infection', 2, 1, 1, '2025-03-18 09:00:00', '2025-03-18 09:30:00'),
    (2, '["Stomach pain"]', NULL, NULL, 2, NULL, NULL, NULL, NULL),
    (3, '["Skin rash"]', NULL, NULL, 1, NULL, NULL, NULL, NULL),
    (4, '["Back pain"]', NULL, NULL, 3, NULL, NULL, NULL, NULL),
    (5, '["Cough", "Sore throat"]', NULL, NULL, 3, NULL, NULL, NULL, NULL);


    
    
DROP DATABASE IF EXISTS doctor;  
CREATE DATABASE `doctor` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `doctor`.`doctor` (
  `doctor_id` INT NOT NULL AUTO_INCREMENT,
  `doctor_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`doctor_id`),
  UNIQUE INDEX `doctor_id_UNIQUE` (`doctor_id` ASC) VISIBLE);
  
  -- Insert fake doctors
INSERT INTO `doctor`.`doctor` (doctor_id, doctor_name)
VALUES 
(1, 'Dr. A'),
(2, 'Dr. B'),
(3, 'Dr. C');
 
DROP DATABASE IF EXISTS prescription;
CREATE DATABASE `prescription` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `prescription`.`prescription` (
  `prescription_id` INT NOT NULL AUTO_INCREMENT,
  `medicine` JSON NOT NULL,
  `appointment_id` INT NOT NULL,
  PRIMARY KEY (`prescription_id`),
  UNIQUE INDEX `prescription_id_UNIQUE` (`prescription_id` ASC) VISIBLE
);

-- Insert fake prescriptions with proper JSON
INSERT INTO `prescription`.`prescription` (medicine, appointment_id) VALUES
('["Paracetamol", "Ibuprofen"]', 1),
('["Antacids", "Oral rehydration salts"]', 2),
('["Antihistamines", "Cortisone cream"]', 3),
('["Painkillers", "Physiotherapy"]', 4),
('["Cough syrup", "Lozenges"]', 5);

CREATE TABLE `prescription`.`medicine` (
  `indiv_medicine` VARCHAR(100) NOT NULL,
  `cost` DECIMAL(5,2) NOT NULL,
  PRIMARY KEY (`indiv_medicine`),
  UNIQUE INDEX `indiv_medicine_UNIQUE` (`indiv_medicine` ASC) VISIBLE
);

-- Insert medication with prices (Correct format)
INSERT INTO `prescription`.`medicine` (indiv_medicine, cost) VALUES
('Paracetamol', 5.00),
('Ibuprofen', 6.50),
('Antacids', 4.00),
('Oral rehydration salts', 3.00),
('Antihistamines', 7.00),
('Cortisone cream', 8.50),
('Painkillers', 6.00),
('Physiotherapy', 50.00),
('Cough syrup', 5.50),
('Lozenges', 3.50),
('Antibiotics', 10.00);


DROP DATABASE IF EXISTS payment;
CREATE DATABASE `payment` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `payment`.`payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `payment_status` tinyint NOT NULL,
  `insurance` tinyint NOT NULL,
  `payment_amount` float NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE INDEX `payment_id_UNIQUE` (`payment_id` ASC) VISIBLE);

-- Insert fake payments
INSERT INTO `payment`.`payment` (appointment_id, payment_status, insurance, payment_amount)
VALUES 
(1, 1, 0, 100.00),
(2, 1, 1, 150.00),
(3, 0, 0, 200.00),
(4, 0, 1, 120.00),
(5, 1, 0, 80.00);









