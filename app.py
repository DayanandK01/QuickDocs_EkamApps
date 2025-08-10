import sqlite3
import os
from flask import Flask, render_template, request, g
from nl_query.converter import natural_language_to_sql  

# --- Configuration ---
DATABASE = 'database/quickdocs.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key'  

# --- Database Helper Functions ---
def get_db():
    """Gets a database connection, or creates one if it doesn't exist."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Routes ---
@app.route('/home')
@app.route('/')
def home():
    """Renders the landing page."""
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def customer_registration():
    """Customer Registration Page & List all customers"""
    db = get_db()
    message = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        process_id = request.form['process']

        cursor = db.execute('SELECT * FROM customers WHERE email = ?', (email,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            message = "Error: A customer with this email already exists."
        else:
            try:
                cursor = db.execute('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
                                    (name, email, phone))
                customer_id = cursor.lastrowid
                db.execute('INSERT INTO process_assignments (customer_id, process_id, status) VALUES (?, ?, ?)',
                           (customer_id, process_id, 'pending'))
                db.commit()
                message = f"Customer '{name}' registered and assigned to a process successfully!"
            except sqlite3.IntegrityError:
                message = "An error occurred. Please check your inputs."

    
    customers = db.execute('SELECT * FROM customers ORDER BY id DESC').fetchall()
    processes = db.execute('SELECT * FROM processes WHERE status = "active"').fetchall()
    return render_template('index.html', customers=customers, processes=processes, message=message)

@app.route('/submission', methods=['GET', 'POST'])
def document_submission():
    """Document Submission Page"""
    db = get_db()
    message = None
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        process_id = request.form['process_id']
        document_type_id = request.form['document_type_id']
        file_url = request.form['file_url']
        ocr_data = request.form['ocr_data']

        try:
            db.execute('INSERT INTO document_submissions (customer_id, process_id, document_type_id, file_url, ocr_data, validation_status) VALUES (?, ?, ?, ?, ?, ?)',
                       (customer_id, process_id, document_type_id, file_url, ocr_data, 'pending'))
            db.commit()
            message = "Document submitted successfully!"

            
            required_docs = db.execute(
                'SELECT COUNT(*) FROM process_required_documents WHERE process_id = ?',
                (process_id,)
            ).fetchone()[0]
            submitted_docs = db.execute(
                'SELECT COUNT(*) FROM document_submissions WHERE customer_id = ? AND process_id = ?',
                (customer_id, process_id)
            ).fetchone()[0]

            completion_percentage = int((submitted_docs / required_docs) * 100) if required_docs > 0 else 0

            db.execute('UPDATE process_assignments SET completion_percentage = ? WHERE customer_id = ? AND process_id = ?',
                       (completion_percentage, customer_id, process_id))
            db.commit()

        except sqlite3.IntegrityError:
            message = "An error occurred. Please check your inputs."

    customers = db.execute('SELECT id, name FROM customers').fetchall()
    processes = db.execute('SELECT id, name FROM processes').fetchall()
    document_types = db.execute('SELECT id, name FROM document_types').fetchall()
    return render_template('submission.html', customers=customers, processes=processes, document_types=document_types, message=message)

@app.route('/dashboard')
def status_dashboard():
    """Status Dashboard Page"""
    db = get_db()
    assignments_query = """
        SELECT
            pa.status,
            pa.completion_percentage,
            c.name as customer_name,
            p.name as process_name,
            (SELECT COUNT(*) FROM process_required_documents prd WHERE prd.process_id = pa.process_id) AS required_docs,
            (SELECT COUNT(*) FROM document_submissions ds WHERE ds.customer_id = pa.customer_id AND ds.process_id = pa.process_id) AS submitted_docs
        FROM process_assignments pa
        JOIN customers c ON pa.customer_id = c.id
        JOIN processes p ON pa.process_id = p.id
        ORDER BY pa.assignment_date DESC;
    """
    assignments = db.execute(assignments_query).fetchall()
    return render_template('dashboard.html', assignments=assignments)

@app.route('/query', methods=['GET', 'POST'])
def query_interface():
    """Natural Language Query Interface"""
    sql_query_text = None
    results = None
    error = None

    if request.method == 'POST':
        nl_query = request.form['nl_query']
        db = get_db()

        sql_query, params = natural_language_to_sql(nl_query)
        if sql_query:
            sql_query_text = sql_query.strip()
            try:
                cursor = db.execute(sql_query, params or [])
                results = cursor.fetchall()
            except sqlite3.Error as e:
                error = f"Database error: {e}"
        else:
            error = "Could not understand your query. Please try one of the supported formats."

    return render_template('query.html', sql_query_text=sql_query_text, results=results, error=error, nl_query=nl_query if 'nl_query' in locals() else None)


if __name__ == '__main__':
    app.run(debug=True)
