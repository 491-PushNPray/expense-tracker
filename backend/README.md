# Expense Tracker Backend

FastAPI REST API for expense categories and transactions, stored in Firebase Cloud Firestore.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and enter the Firebase project ID and absolute path to a Firebase service account JSON file.

4. Start the API from this directory:

   ```bash
   uvicorn app.main:app --reload
   ```

The API runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.
