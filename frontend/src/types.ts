type TransactionType = "income" | "expense";

interface CategoryInput {
  name: string;
  type: TransactionType;
  is_default: boolean;
}

interface Category extends CategoryInput {
  id: string;
}

interface TransactionInput {
  amount: number;
  type: TransactionType;
  date: string;
  description: string | null;
  category_id: string;
}

interface Transaction extends TransactionInput {
  id: string;
  created_at: string;
  updated_at: string;
}

interface TransactionForm {
  amount: number | null;
  type: TransactionType;
  date: Date;
  description: string;
  category_id: string;
}
