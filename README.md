# 📝 Task Management Application (CLI)

A command-line **Task Management Application** built with **Python** and **PostgreSQL**.  
This app helps users manage their daily tasks by providing features to add, update, view, and delete tasks.

---

## 🚀 Features

- Add a new task with details (title, description, due date, priority).
- List all tasks with optional filtering:
  - By **due date**
  - By **priority**
  - By **status**
- Update task details (title, description, due date, priority, status).
- Mark tasks as **completed**.
- Delete tasks.
- Automatically tracks:
  - **Task ID** (unique identifier)
  - **Creation timestamp**

---

## 📂 Task Attributes

Each task includes the following fields:

- **Task ID** (unique identifier)
- **Title**
- **Description**
- **Due Date**
- **Priority Level** (Low | Medium | High)
- **Status** (Pending | In Progress | Completed)
- **Creation Timestamp**

---

## 🛠️ Tech Stack

- **Python** (CLI application logic)
- **PostgreSQL** (database for task storage)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/task-manager-cli.git
cd task-manager-cli
