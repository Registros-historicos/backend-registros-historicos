from django.db import connection

def call_function(query: str, params=None):
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if cursor.description:
            cols = [c[0] for c in cursor.description]
            return [dict(zip(cols, row)) for row in cursor.fetchall()]
        return []
