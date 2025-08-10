-- Processes Table
CREATE TABLE processes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document Types Table
CREATE TABLE document_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    required_fields TEXT -- Stored as a JSON string
);

-- Customers Table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Process Assignments Table
CREATE TABLE process_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    process_id INTEGER,
    assignment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending',
    completion_percentage INTEGER DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (process_id) REFERENCES processes(id) ON DELETE CASCADE,
    UNIQUE(customer_id, process_id)
);

-- Document Submissions Table
CREATE TABLE document_submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    process_id INTEGER,
    document_type_id INTEGER,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_url TEXT,
    ocr_data TEXT,
    validation_status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    FOREIGN KEY (process_id) REFERENCES processes(id) ON DELETE CASCADE,
    FOREIGN KEY (document_type_id) REFERENCES document_types(id) ON DELETE CASCADE
);

-- Process Required Documents Table (Many-to-Many relationship)
CREATE TABLE process_required_documents (
    process_id INTEGER NOT NULL,
    document_type_id INTEGER NOT NULL,
    PRIMARY KEY (process_id, document_type_id),
    FOREIGN KEY (process_id) REFERENCES processes(id) ON DELETE CASCADE,
    FOREIGN KEY (document_type_id) REFERENCES document_types(id) ON DELETE CASCADE
);
