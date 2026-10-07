# Expense Tracker

A simple expense-tracking web application built with a Python backend, an Angular and TypeScript frontend, and Firebase as the database.

## Features

- Create, view, update, and delete transactions
- Organize transactions by category
- Track income and expenses
- Store transaction dates and descriptions
- Provide default and custom categories
- No authentication required

## Tech Stack

- **Frontend:** Angular, TypeScript
- **Backend:** Python
- **Database:** Firebase
- **API:** REST

## Database Schema

### Transactions

| Field | Description |
|---|---|
| `id` | Unique transaction identifier |
| `amount` | Transaction amount |
| `type` | Transaction type, such as `income` or `expense` |
| `date` | Date of the transaction |
| `created_at` | Timestamp when the transaction was created |
| `updated_at` | Timestamp when the transaction was last updated |
| `description` | Optional description of the transaction |
| `category_id` | ID of the associated category |

### Categories

| Field | Description |
|---|---|
| `id` | Unique category identifier |
| `name` | Category name |
| `type` | Category type, such as `income` or `expense` |
| `is_default` | Whether the category is provided by default |

## API Endpoints

### Transactions

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/transactions` | Get all transactions |
| `GET` | `/transactions/{id}` | Get a transaction by ID |
| `POST` | `/transactions` | Create a transaction |
| `PUT` | `/transactions/{id}` | Update a transaction |
| `DELETE` | `/transactions/{id}` | Delete a transaction |

### Categories

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/categories` | Get all categories |
| `GET` | `/categories/{id}` | Get a category by ID |
| `POST` | `/categories` | Create a category |
| `PUT` | `/categories/{id}` | Update a category |
| `DELETE` | `/categories/{id}` | Delete a category |
