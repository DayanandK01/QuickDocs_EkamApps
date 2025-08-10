-- Insert 2 Processes
INSERT INTO processes (name, description, status) VALUES
('Home Loan Application', 'Process for submitting documents for a home loan.', 'active'),
('KYC Verification', 'Standard Know Your Customer verification process.', 'active');

-- Insert 5 Document Types
INSERT INTO document_types (name, description, required_fields) VALUES
('PAN Card', 'Permanent Account Number Card', '{"fields": ["PAN_number", "name", "date_of_birth"]}'),
('Salary Slip', 'Recent salary slip from employer', '{"fields": ["employee_name", "gross_salary", "net_salary"]}'),
('Bank Statement', 'Bank account statement for the last 6 months', '{"fields": ["account_holder_name", "account_number"]}'),
('Aadhaar Card', 'Indian government identification card', '{"fields": ["aadhaar_number", "name", "address"]}'),
('Passport', 'Valid passport for identity verification', '{"fields": ["passport_number", "full_name"]}');

-- Link documents to processes as per the test scenario
-- Process 1: Home Loan Application requires PAN Card, Salary Slip, Bank Statement
INSERT INTO process_required_documents (process_id, document_type_id) VALUES
(1, 1),
(1, 2),
(1, 3);

-- Process 2: KYC Verification requires PAN Card, Aadhaar Card
INSERT INTO process_required_documents (process_id, document_type_id) VALUES
(2, 1),
(2, 4);

-- Insert 5 Customers with Indian names
INSERT INTO customers (name, email, phone) VALUES
('Anjali Sharma', 'anjali.sharma@example.com', '9876543210'),
('Rahul Singh', 'rahul.singh@example.com', '9988776655'),
('Priya Gupta', 'priya.gupta@example.com', '9012345678'),
('Amit Patel', 'amit.patel@example.com', '9123456789'),
('Sneha Verma', 'sneha.verma@example.com', '9234567890');

-- Assign customers to processes with mixed statuses
-- Anjali has submitted 1 of 3 docs for Home Loan, so she's 'in-progress'
INSERT INTO process_assignments (customer_id, process_id, status, completion_percentage) VALUES
(1, 1, 'in-progress', 33), 
(2, 1, 'pending', 0),
(3, 2, 'pending', 0),
(4, 2, 'in-progress', 50), 
(5, 2, 'pending', 0);

-- Insert some sample document submissions
-- Anjali submits her PAN Card for the Home Loan
INSERT INTO document_submissions (customer_id, process_id, document_type_id, file_url, ocr_data) VALUES
(1, 1, 1, 'http://example.com/docs/anjali_pan.pdf', '{"PAN_number": "ABCDE1234F", "name": "Anjali Sharma"}');

-- Amit submits his PAN Card for KYC
INSERT INTO document_submissions (customer_id, process_id, document_type_id, file_url, ocr_data) VALUES
(4, 2, 1, 'http://example.com/docs/amit_pan.pdf', '{"PAN_number": "FGHIJ5678K", "name": "Amit Patel"}');

-- A customer for whom all documents are submitted for a process
INSERT INTO customers (name, email, phone) VALUES
('Rajiv Kumar', 'rajiv.kumar@example.com', '9999999999');

INSERT INTO process_assignments (customer_id, process_id, status, completion_percentage) VALUES
(6, 2, 'completed', 100);

-- Rajiv submits both required documents for KYC
INSERT INTO document_submissions (customer_id, process_id, document_type_id, file_url, ocr_data) VALUES
(6, 2, 1, 'http://example.com/docs/rajiv_pan.pdf', '{"PAN_number": "LMNOP1234Q", "name": "Rajiv Kumar"}'),
(6, 2, 4, 'http://example.com/docs/rajiv_aadhaar.pdf', '{"aadhaar_number": "123456789012", "name": "Rajiv Kumar"}');
