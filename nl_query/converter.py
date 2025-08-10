import re

def natural_language_to_sql(query):
    """
    Converts a natural language query into a SQL statement 
    using a simple rule-based approach.
    """
    query_lower = query.lower().strip()
    sql_query = None
    params = []

    if query_lower in ["show all customers", "list all customers"]:
        sql_query = "SELECT * FROM customers;"
        return sql_query, params

    if re.match(r"^(list|show)\s+all\s+pending\s+processes\??$", query_lower):
        sql_query = """
            SELECT p.name AS process_name, COUNT(*) AS pending_count
            FROM process_assignments pa
            JOIN processes p ON pa.process_id = p.id
            WHERE pa.status = 'pending'
            GROUP BY p.name;
        """
        return sql_query, params

    match = re.match(r"how many documents (?:has|did) (.*) submitted\??", query_lower)
    if match:
        customer_name = match.group(1).strip()
        sql_query = """
            SELECT COUNT(ds.id) AS documents_submitted
            FROM document_submissions ds
            JOIN customers c ON ds.customer_id = c.id
            WHERE LOWER(c.name) = LOWER(?);
        """
        params.append(customer_name)
        return sql_query, params

    if re.match(r"which process has the most documents\??", query_lower):
        sql_query = """
            SELECT p.name AS process_name, COUNT(ds.id) as document_count
            FROM document_submissions ds
            JOIN processes p ON ds.process_id = p.id
            GROUP BY p.name
            ORDER BY document_count DESC
            LIMIT 1;
        """
        return sql_query, params

    match = re.match(r"which customers are (?:assigned to|on) (.+?)\??$", query_lower)
    if match:
        process_name = match.group(1).strip().rstrip("?")
        sql_query = """
            SELECT DISTINCT c.name AS customer_name
            FROM customers c
            JOIN process_assignments pa ON c.id = pa.customer_id
            JOIN processes p ON pa.process_id = p.id
            WHERE LOWER(p.name) = LOWER(?);
        """
        params.append(process_name)
        return sql_query, params

    if re.match(r"^(show|list) all document types\??$", query_lower):
        sql_query = "SELECT * FROM document_types;"
        return sql_query, params

    if re.match(r"how many customers (?:are registered|do we have)\??$", query_lower):
        sql_query = "SELECT COUNT(*) AS customer_count FROM customers;"
        return sql_query, params

    if re.match(r"^(list|show) all completed processes\??$", query_lower):
        sql_query = """
            SELECT p.name AS process_name, COUNT(*) AS completed_count
            FROM process_assignments pa
            JOIN processes p ON pa.process_id = p.id
            WHERE pa.status = 'completed'
            GROUP BY p.name;
        """
        return sql_query, params

    if re.match(r"which customer has submitted the most documents\??$", query_lower):
        sql_query = """
            SELECT c.name AS customer_name, COUNT(ds.id) AS document_count
            FROM document_submissions ds
            JOIN customers c ON ds.customer_id = c.id
            GROUP BY c.name
            ORDER BY document_count DESC
            LIMIT 1;
        """
        return sql_query, params

    if re.match(r"show all processes and their required documents\??$", query_lower):
        sql_query = """
            SELECT p.name AS process_name, dt.name AS document_type
            FROM processes p
            JOIN process_required_documents prd ON p.id = prd.process_id
            JOIN document_types dt ON prd.document_type_id = dt.id
            ORDER BY p.name, dt.name;
        """
        return sql_query, params

    return None, None
