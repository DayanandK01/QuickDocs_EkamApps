# QuickDocs

QuickDocs is a lightweight document management and process tracking system built with Flask and SQLite.  
It allows:
- Customer registration & process assignment
- Document submissions with progress tracking
- A dashboard to view process statuses
- A natural language query interface to search the database

## Features
- **Customer Management** – Register customers and assign them to processes.
- **Document Submission** – Upload document details and track completion.
- **Process Dashboard** – View progress and statuses at a glance.
- **Natural Language Queries** – Query the database using everyday language.

## Project Structure
```
└── 📁application
    └── 📁database
        ├── ER_diagram_quickdocs.png
        ├── init_db.py
        ├── quickdocs.db
        ├── sample_data.sql
        ├── schema.sql
    └── 📁nl_query
        └── 📁__pycache__
            ├── __init__.cpython-313.pyc
            ├── converter.cpython-313.pyc
        ├── __init__.py
        ├── converter.py
        ├── nl_query_example.txt
    └── 📁screenshots
        ├── CustomerRegistratoin.png
        ├── Dashboard.png
        ├── DocumentSubmission.png
        ├── HomePage.png
        ├── NL_query_01.png
        ├── NL_query_02.png
        ├── NL_query_03.png
        ├── NL_query_04.png
        ├── NL_query_05.png
        ├── NL_query_06.png
        ├── NL_query_error.png
    └── 📁templates
        ├── dashboard.html
        ├── home.html
        ├── index.html
        ├── query.html
        ├── submission.html
    ├── app.py
    ├── README.md
    └── requirements.txt
```

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/DayanandK01/QuickDocs_EkamApps.git
cd quickdocs
```


### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. initialize the database
```bash
sqlite3 database/quickdocs.db < schema.sql
```

### 4. Run the application
```bash
python app.py
```
