import psycopg2
from datetime import datetime
from db_utils import connect_db

# database connection
conn = connect_db()

def add_task():
    print('Add Task')
    title = input('Title: ')
    if not title:
        print('Title cannot be empty')
        return
    descrip = input('Description: ').strip()
    due_date = input('Enter due date (YYYY-MM-DD): ')
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid format! Use YYYY-MM-DD")
            return

    print('Priority Levels: Low, Medium, High\n')
    priority = input('Enter Priority Level: ')
    if priority not in ['Low', 'Medium', 'High']:
        priority = 'Low'
    print('Status: Pending, In Progress, Completed')
    status = input('Enter Status: ')
    if status not in ['Pending', 'In Progress', 'Completed']:
        status = 'Pending'

    # insert into database
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (
                title,
                description,
                due_date,
                priority,
                status,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING task_id;
        """, (
            title,
            descrip,
            due_date,
            priority,
            status
        ))
        conn.commit()
    except psycopg2.Error as e:
        print(f'Error adding to the database: {e}')

def list_tasks():
    print("\nList Tasks")
    print("Filter options:")
    print("1. All tasks")
    print("2. By status")
    print("3. By priority")
    print("4. By due date range")
    
    choice = input("Choose filter option (1-4): ").strip()
    
    base_query = """
    SELECT task_id, title, description, due_date, priority, status, created_at
    FROM tasks
    """
    params = []
    
    if choice == "2":
        print("Status options: Pending, In Progress, Completed")
        status = input("Enter status: ").strip()
        if status in ['Pending', 'In Progress', 'Completed']:
            base_query += " WHERE status = %s"
            params.append(status)
    
    elif choice == "3":
        print("Priority options: Low, Medium, High")
        priority = input("Enter priority: ").strip()
        if priority in ['Low', 'Medium', 'High']:
            base_query += " WHERE priority = %s"
            params.append(priority)
    
    elif choice == "4":
        start_date = input("Enter start date (YYYY-MM-DD, optional): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD, optional): ").strip()
        
        conditions = []
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                conditions.append("due_date >= %s")
                params.append(start_date)
            except ValueError:
                print("Invalid start date format!")
                return
        
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
                conditions.append("due_date <= %s")
                params.append(end_date)
            except ValueError:
                print("Invalid end date format!")
                return
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
    
    base_query += " ORDER BY task_id"
    
    try:
        cursor = conn.cursor()
        
        cursor.execute(base_query, params)
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found.")
        else:
            print(f"\nFound {len(tasks)} task(s):")
            print("-" * 100)
            print(f"{'ID':<4} {'Title':<20} {'Due Date':<12} {'Priority':<8} {'Status':<12} {'Created':<20}")
            print("-" * 100)
            
            for task in tasks:
                task_id, title, description, due_date, priority, status, created_at = task
                due_str = due_date.strftime('%Y-%m-%d') if due_date else 'N/A'
                created_str = created_at.strftime('%Y-%m-%d %H:%M')
                title_short = title[:18] + '..' if len(title) > 20 else title
                
                print(f"{task_id:<4} {title_short:<20} {due_str:<12} {priority:<8} {status:<12} {created_str:<20}")
                
                if description:
                    print(f"     Description: {description}")
                print()
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error listing tasks: {e}")

def update_task():
    print("\nUpdate Task")
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Invalid task ID!")
        return
    
    # First check if task exists
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            print("Task not found!")
            cursor.close()
            conn.close()
            return
        
        print("Current task details:")
        print(f"Title: {task[1]}")
        print(f"Description: {task[2] or 'N/A'}")
        print(f"Due Date: {task[3] or 'N/A'}")
        print(f"Priority: {task[4]}")
        print(f"Status: {task[5]}")
        
        print("\nEnter new values (press Enter to keep current value):")
        
        new_title = input(f"Title [{task[1]}]: ").strip()
        new_description = input(f"Description [{task[2] or ''}]: ").strip()
        new_due_date = input(f"Due Date [{task[3] or ''}] (YYYY-MM-DD): ").strip()
        
        print("Priority options: Low, Medium, High")
        new_priority = input(f"Priority [{task[4]}]: ").strip()
        
        print("Status options: Pending, In Progress, Completed")
        new_status = input(f"Status [{task[5]}]: ").strip()
        
        # Use current values if nothing entered
        if not new_title:
            new_title = task[1]
        if not new_description:
            new_description = task[2]
        if not new_due_date:
            new_due_date = task[3]
        else:
            try:
                datetime.strptime(new_due_date, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format!")
                cursor.close()
                conn.close()
                return
        
        if not new_priority or new_priority not in ['Low', 'Medium', 'High']:
            new_priority = task[4]
        if not new_status or new_status not in ['Pending', 'In Progress', 'Completed']:
            new_status = task[5]
        
        update_query = """
        UPDATE tasks 
        SET title = %s, description = %s, due_date = %s, priority = %s, status = %s
        WHERE task_id = %s
        """
        
        cursor.execute(update_query, (new_title, new_description, new_due_date, new_priority, new_status, task_id))
        conn.commit()
        
        print("Task updated successfully!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error updating task: {e}")

def task_complete():
    print("\nMark Task as Completed")
    try:
        task_id = int(input("Enter task ID to mark as completed: "))
    except ValueError:
        print("Invalid task ID!")
        return
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, status FROM tasks WHERE task_id = %s", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            print("Task not found!")
        elif task[1] == 'Completed':
            print(f"Task '{task[0]}' is already completed!")
        else:
            cursor.execute("UPDATE tasks SET status = 'Completed' WHERE task_id = %s", (task_id,))
            conn.commit()
            print(f"Task '{task[0]}' marked as completed!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error marking task as completed: {e}")

def del_task():
    print("\nDelete Task")
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid task ID!")
        return
    
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT title FROM tasks WHERE task_id = %s", (task_id,))
        task = cursor.fetchone()
        
        if not task:
            print("Task not found!")
        else:
            confirm = input(f"Are you sure you want to delete task '{task[0]}'? (y/N): ").strip().lower()
            if confirm == 'y':
                cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
                conn.commit()
                print("Task deleted successfully!")
            else:
                print("Deletion cancelled.")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error deleting task: {e}")

def main():

    while True:
        print('Welcome to the Task Management App')
        choice = int(input('[1] Add Task\n[2] Task List\n[3] Update\n[4] Status\n[5] Delete\n[6] Exit\nEnter:'))
        if choice == 1: add_task()
        elif choice == 2: list_tasks()
        elif choice == 3: update_task()
        elif choice == 4: task_complete()
        elif choice == 5: del_task()
        elif choice == 6: return
        else:
            print('Invalid input')


main()