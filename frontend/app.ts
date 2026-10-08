type TransactionType = "income" | "expense";
interface CategoryInput {
  name: string;
  type: TransactionType;
  is_default: boolean;
}
interface Category extends CategoryInput { id: string; }
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

class ExpenseController {
  static $inject = ["$http"];
  private readonly api = "http://localhost:8000";
  categories: Category[] = [];
  transactions: Transaction[] = [];
  categoryForm = this.emptyCategory();
  transactionForm = this.emptyTransaction();
  editingCategoryId: string | null = null;
  editingTransactionId: string | null = null;
  busy = false;
  error = "";

  constructor(private $http: angular.IHttpService) {
    this.reload();
  }

  private emptyCategory(): CategoryInput {
    return { name: "", type: "expense", is_default: false };
  }

  private emptyTransaction(): TransactionForm {
    return { amount: null, type: "expense", date: new Date(), description: "", category_id: "" };
  }

  private refresh(): angular.IPromise<void> {
    return this.$http.get<Category[]>(`${this.api}/categories`).then(response => {
      this.categories = response.data;
      return this.$http.get<Transaction[]>(`${this.api}/transactions`);
    }).then(response => {
      this.transactions = response.data;
    });
  }

  private run(action: () => angular.IPromise<unknown>, reload = true): void {
    if (this.busy) return;
    this.busy = true;
    this.error = "";
    action().then(() => reload ? this.refresh() : undefined)
      .catch((error: angular.IHttpResponse<unknown>) => {
        const data = error.data as { detail?: string | Array<{ msg: string }> } | null;
        const detail = data?.detail;
        this.error = typeof detail === "string" ? detail
          : Array.isArray(detail) ? detail.map(item => item.msg).join(". ")
          : "Request failed. Check that the backend is running.";
      }).finally(() => { this.busy = false; });
  }

  reload(): void { this.run(() => this.refresh(), false); }

  private total(type: TransactionType): number {
    return this.transactions.filter(t => t.type === type).reduce((sum, t) => sum + t.amount, 0);
  }
  get income(): number { return this.total("income"); }
  get expenses(): number { return this.total("expense"); }
  get balance(): number { return this.income - this.expenses; }

  matchingCategories(): Category[] {
    return this.categories.filter(c => c.type === this.transactionForm.type);
  }

  categoryName(id: string): string {
    return this.categories.find(c => c.id === id)?.name ?? "Unknown category";
  }

  saveCategory(): void {
    const payload = { ...this.categoryForm, name: this.categoryForm.name.trim() };
    if (!payload.name) { this.error = "Enter a category name."; return; }
    const id = this.editingCategoryId;
    this.run(() => {
      const request = id
        ? this.$http.put(`${this.api}/categories/${encodeURIComponent(id)}`, payload)
        : this.$http.post(`${this.api}/categories`, payload);
      return request.then(() => this.cancelCategory());
    });
  }

  editCategory(id: string): void {
    this.run(() => this.$http.get<Category>(`${this.api}/categories/${encodeURIComponent(id)}`)
      .then(({ data }) => {
        this.editingCategoryId = data.id;
        this.categoryForm = { name: data.name, type: data.type, is_default: data.is_default };
      }), false);
  }

  deleteCategory(id: string): void {
    this.run(() => this.$http.delete(`${this.api}/categories/${encodeURIComponent(id)}`)
      .then(() => {
        if (this.editingCategoryId === id) this.cancelCategory();
        if (this.transactionForm.category_id === id) this.transactionForm.category_id = "";
      }));
  }

  cancelCategory(): void {
    this.editingCategoryId = null;
    this.categoryForm = this.emptyCategory();
  }

  saveTransaction(): void {
    const form = this.transactionForm;
    if (form.amount == null || !Number.isFinite(form.amount) || form.amount <= 0 ||
        !form.category_id || !(form.date instanceof Date) || Number.isNaN(form.date.getTime())) {
      this.error = "Enter a positive amount, a date, and a category.";
      return;
    }
    // Keep the selected local calendar date when sending it to the API.
    const year = form.date.getFullYear();
    const month = String(form.date.getMonth() + 1).padStart(2, "0");
    const day = String(form.date.getDate()).padStart(2, "0");
    const payload: TransactionInput = {
      amount: form.amount, type: form.type, date: `${year}-${month}-${day}`,
      description: form.description.trim() || null, category_id: form.category_id
    };
    const id = this.editingTransactionId;
    this.run(() => {
      const request = id
        ? this.$http.put(`${this.api}/transactions/${encodeURIComponent(id)}`, payload)
        : this.$http.post(`${this.api}/transactions`, payload);
      return request.then(() => this.cancelTransaction());
    });
  }

  editTransaction(id: string): void {
    this.run(() => this.$http.get<Transaction>(`${this.api}/transactions/${encodeURIComponent(id)}`)
      .then(({ data }) => {
        const [year, month, day] = data.date.split("-").map(Number);
        this.editingTransactionId = data.id;
        this.transactionForm = {
          amount: data.amount, type: data.type, date: new Date(year, month - 1, day),
          description: data.description ?? "", category_id: data.category_id
        };
      }), false);
  }

  deleteTransaction(id: string): void {
    this.run(() => this.$http.delete(`${this.api}/transactions/${encodeURIComponent(id)}`)
      .then(() => {
        if (this.editingTransactionId === id) this.cancelTransaction();
      }));
  }

  cancelTransaction(): void {
    this.editingTransactionId = null;
    this.transactionForm = this.emptyTransaction();
  }
}

angular.module("expenseApp", []).controller("ExpenseController", ExpenseController);
