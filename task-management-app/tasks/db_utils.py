import psycopg2

def connect_db():
    print('Connecting to database')
    try:
        conn = psycopg2.connect(
            host='localhost',
            dbname='task_management',
            port=5432,
            user='db_user',
            password='db_password'
        )
        conn.commit()
        return conn
    except psycopg2.Error as e:
        print(f'Error connecting to database: {e}')

def create_table():
    print('Creating Table')
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        task_id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date DATE,
        priority TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    )
    """)
    conn.commit()
    try:
        pass
    except psycopg2.Error as e:
        print(f'Error creating table:{e}')