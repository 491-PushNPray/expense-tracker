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

3. Create a `.env` file in this directory with your Firebase project ID and the absolute path to your service account JSON file:

   ```env
   FIREBASE_PROJECT_ID=your-project-id
   GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/backend/firebase-service-account.json
   ```

4. Start the API from this directory:

   ```bash
   uvicorn app.main:app --reload
   ```

The API runs at `http://localhost:8000`. Interactive API documentation is available at `http://localhost:8000/docs`.
