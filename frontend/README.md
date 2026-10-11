# Expense Tracker Frontend

A basic AngularJS 1.8.3 and TypeScript page for the existing FastAPI backend.
It supports category and transaction CRUD, totals, and backend error messages.
There is no authentication.

## Run

Start the configured backend on http://localhost:8000 using the backend README.
Then, from this directory:

```bash
npm install
npm start
```

Open http://localhost:4200 (the backend's default allowed frontend origin).
`npm start` compiles TypeScript and serves static files using Python 3.
Node/npm provide development tools; the API server remains Python/FastAPI.

For automatic recompilation while editing, run `npm run watch` in another terminal.

## Files

- `index.html`: page structure and AngularJS template bindings.
- `styles.css`: layout, typography, responsive rules, and component styling.
- `src/types.ts`: shared frontend data types.
- `src/expense-controller.ts`: form state, API calls, and UI behavior.
- `src/app.ts`: AngularJS module and controller registration.
- `dist/`: generated browser scripts; ignored by Git.
- `tsconfig.json`: TypeScript compiler settings.

## Checks

```bash
npm run typecheck
```

Categories must match a transaction's type. The backend blocks deleting a category
that has transactions, or changing its type while it is in use. These errors are
shown on the page. PUT requests include the full editable record; transaction
IDs and timestamps are managed by the backend.
