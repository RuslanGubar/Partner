import psycopg2

def connect_to_database():
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin",
                                host="localhost", port="5432")
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка соединения с бд: {e}")
        return None

def execute_query(conn, query, params=None):
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        return cur
    except psycopg2.Error as e:
        print(f"Ошибка при выполнении запроса: {e}")
        conn.rollback()
        return None