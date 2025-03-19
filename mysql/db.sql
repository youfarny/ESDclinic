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
  PRIMARY KEY (`patient_id`),
  UNIQUE INDEX `patient_id_UNIQUE` (`patient_id` ASC) VISIBLE);
  
  -- Insert fake patients
INSERT INTO `patient`.`patient` (patient_name, patient_password, patient_contact, patient_address, patient_insurance, patient_allergies)
VALUES 
('John Doe', 'password123', 987654321, '123 Main St', 1, '["Penicillin"]'),
('Jane Smith', 'securepass', 876543210, '456 Oak St', 0, '["None"]'),
('Alice Johnson', 'alicepass', 765432109, '789 Pine St', 1, '["Peanuts"]'),
('Bob Williams', 'bobpass', 654321098, '101 Maple St', 0, '["Sulfa drugs"]'),
('Emily Brown', 'emilypass', 543210987, '202 Birch St', 1, '["None"]');
  
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
(1, 1, 12345678),
(2, 2, 12345678),
(3, 3, 12345678),
(4, 1, 12345678),
(5, 2, 12345678);

DROP DATABASE IF EXISTS appointment;  
CREATE DATABASE `appointment` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `appointment`.`appointment` (
  `appointment_id` INT NOT NULL AUTO_INCREMENT,
  `patient_id` INT NOT NULL,
  `patient_symptoms` LONGTEXT NOT NULL,
  `notes` LONGTEXT NULL,
  `diagnosis` LONGTEXT NULL,
  `doctor_id` INT NULL,
  `prescription_id` INT NULL,
  `payment_id` INT NULL,
  `start_time` DATETIME NULL,
  `end_time` DATETIME NULL,
  PRIMARY KEY (`appointment_id`),
  UNIQUE INDEX `appointment_id_UNIQUE` (`appointment_id` ASC) VISIBLE);
  
  -- Insert fake appointments
INSERT INTO `appointment`.`appointment` 
    (patient_id, patient_symptoms, notes, diagnosis, doctor_id, prescription_id, payment_id, start_time, end_time)
VALUES 
    (1, 'Fever, headache', 'Mild fever observed', 'Viral infection', 1, 1, 1, '2025-03-18 09:00:00', '2025-03-18 09:30:00'),
    (2, 'Stomach pain', 'Abdominal tenderness', 'Food poisoning', 2, 2, 2, '2025-03-18 10:00:00', '2025-03-18 10:20:00'),
    (3, 'Skin rash', 'Red patches on skin', 'Allergic reaction', 3, 3, 3, '2025-03-18 11:00:00', '2025-03-18 11:15:00'),
    (4, 'Back pain', 'Lower back discomfort', 'Muscle strain', 1, 4, 4, '2025-03-18 13:00:00', '2025-03-18 13:45:00'),
    (5, 'Cough and sore throat', 'Mild throat redness', 'Common cold', 2, 5, 5, '2025-03-18 14:00:00', '2025-03-18 14:30:00');
    
    
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
(1, 'Dr. Michael Lee'),
(2, 'Dr. Susan Davis'),
(3, 'Dr. Robert Wilson');
 
DROP DATABASE IF EXISTS prescription;
CREATE DATABASE `prescription` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `prescription`.`prescription` (
  `prescription_id` INT NOT NULL AUTO_INCREMENT,
  `medicine` VARCHAR(100) NOT NULL,
  `appointment_id` INT NOT NULL,
  PRIMARY KEY (`prescription_id`),
  UNIQUE INDEX `prescription_id_UNIQUE` (`prescription_id` ASC) VISIBLE);
  
  -- Insert fake prescriptions
INSERT INTO `prescription`.`prescription` (prescription_id, medicine, appointment_id)
VALUES 
(1, 'Paracetamol, Ibuprofen', '1'),
(2, 'Antacids, Oral rehydration salts', '2'),
(3, 'Antihistamines, Cortisone cream', '3'),
(4, 'Painkillers, Physiotherapy', '4'),
(5, 'Cough syrup, Lozenges', '5');

DROP DATABASE IF EXISTS payment;
CREATE DATABASE `payment` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `payment`.`payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `payment_status` tinyint NOT NULL,
  `payment_amount` float NOT NULL,
  PRIMARY KEY (`payment_id`),
  UNIQUE INDEX `payment_id_UNIQUE` (`payment_id` ASC) VISIBLE);

-- Insert fake payments
INSERT INTO `payment`.`payment` (payment_id, appointment_id, payment_status, payment_amount)
VALUES 
(1, 1, 1, '100.00'),
(2, 2, 1, '150.00'),
(3, 3, 0, '200.00'),
(4, 4, 1, '120.00'),
(5, 5, 1, '80.00');








