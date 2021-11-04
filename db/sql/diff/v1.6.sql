
CREATE TABLE Communication (
    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	addresses TEXT,
	subject VARCHAR(255) NOT NULL,
	body TEXT NOT NULL,
	status enum('DRAFT', 'PROCESSED') NOT NULL DEFAULT 'DRAFT',
	sys_date timestamp NULL DEFAULT CURRENT_TIMESTAMP
);