# Streaming Hub - Setup Guide

Follow these steps to get your OTT project running.

## 1. Prerequisites
- Python installed on your system.
- VS Code or any text editor.

## 2. Installation
Open your terminal in the project directory and run:

```bash
# Install dependencies
pip install -r requirements.txt
```

## 3. Running the Project
Execute the `run.py` script:

```bash
python run.py
```

- On the first run, the system will automatically:
  - Create the tables in the **MySQL** database.
  - Create a default Admin account.
  - Add sample movies.

> [!IMPORTANT]
> Make sure you create the database named `streaming_hub` in your MySQL server before running the project:
> `CREATE DATABASE streaming_hub;`

## 4. Default Credentials
| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@streamhub.com | admin123 |

## 5. Usage
- **Home**: View all movies.
- **Login/Register**: Access personal accounts.
- **Watch**: Requires a subscription.
- **Subscription**: Simple button to activate premium access for testing.
- **Admin Panel**: Accessible only to admin users to add/delete movies and view users.
