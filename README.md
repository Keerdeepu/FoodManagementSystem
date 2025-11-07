# Food Recipe Management System

## Prerequisites
- Python 3.10+
- MySQL server
- pip

## Setup
1. Clone repo
2. Create virtual env
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Set up MySQL
   - Run `sql/schema.sql` and `sql/seed_data.sql` or use ORM seeding:
     mysql -u root -p < sql/schema.sql
     mysql -u root -p < sql/seed_data.sql

5. Create `.env` file:
   DB_USER=root
   DB_PASS=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=recipe_db

6. (Optional) seed data via Python ORM:
   python -c "import app.seed; app.seed.seed()"

7. Run FastAPI:
   uvicorn app.main:app --reload --port 8000

8. API docs:
   Visit http://127.0.0.1:8000/docs

## Reporting
Run:
   python reports/reports.py
