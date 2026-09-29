from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class PayrollSystem:
    def __init__(self, master):
        self.master = master
        master.title("Employee Payroll Management System")
        master.geometry("700x500")
        master.resizable(False, False)
        master.configure(bg="#e3f2fd")

        # Connect DB
        self.conn = sqlite3.connect("payroll.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Tkinter Variables
        self.name_var = StringVar()
        self.basic_var = DoubleVar()
        self.allow_var = DoubleVar()
        self.deduct_var = DoubleVar()
        self.netpay_var = DoubleVar()

        self.create_widgets()
        self.load_table()

        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                basic REAL,
                allowance REAL,
                deductions REAL,
                netpay REAL
            )
        """)
        self.conn.commit()

    def create_widgets(self):
        header = Label(self.master, text="Employee Payroll Management", font=("Helvetica", 16, "bold"),
                       bg="#1976d2", fg="white")
        header.pack(pady=15, fill=X)

        form = Frame(self.master, bg="#e3f2fd")
        form.pack(pady=10)

        Label(form, text="Name:", font=("Arial", 12), bg="#e3f2fd").grid(row=0, column=0, padx=10, pady=5, sticky=E)
        Entry(form, textvariable=self.name_var, font=("Arial", 12), width=20).grid(row=0, column=1, padx=10, pady=5)

        Label(form, text="Basic Pay:", font=("Arial", 12), bg="#e3f2fd").grid(row=1, column=0, padx=10, pady=5, sticky=E)
        Entry(form, textvariable=self.basic_var, font=("Arial", 12), width=20).grid(row=1, column=1, padx=10, pady=5)

        Label(form, text="Allowance:", font=("Arial", 12), bg="#e3f2fd").grid(row=2, column=0, padx=10, pady=5, sticky=E)
        Entry(form, textvariable=self.allow_var, font=("Arial", 12), width=20).grid(row=2, column=1, padx=10, pady=5)

        Label(form, text="Deductions:", font=("Arial", 12), bg="#e3f2fd").grid(row=3, column=0, padx=10, pady=5, sticky=E)
        Entry(form, textvariable=self.deduct_var, font=("Arial", 12), width=20).grid(row=3, column=1, padx=10, pady=5)

        Button(form, text="Calculate & Add", font=("Arial", 12, "bold"), bg="#64b5f6", fg="white",
               command=self.add_employee).grid(row=4, column=0, columnspan=2, pady=10)

        # Payroll Table
        self.table_frame = Frame(self.master, bg="#e3f2fd")
        self.table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("Name", "Basic", "Allowance", "Deduction", "Net Pay"), show="headings")
        for col in ("Name", "Basic", "Allowance", "Deduction", "Net Pay"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110, anchor="center")
        self.tree.pack(fill=BOTH, expand=True)

    def add_employee(self):
        name = self.name_var.get().strip()
        try:
            basic = float(self.basic_var.get())
            allow = float(self.allow_var.get())
            deduct = float(self.deduct_var.get())
        except ValueError:
            messagebox.showerror("Invalid Entry", "Enter numeric values for pay, allowance and deductions.")
            return

        if not name:
            messagebox.showerror("Invalid Entry", "Name cannot be empty.")
            return

        netpay = basic + allow - deduct
        self.netpay_var.set(netpay)

        self.cursor.execute(
            "INSERT INTO payroll (name, basic, allowance, deductions, netpay) VALUES (?, ?, ?, ?, ?)",
            (name, basic, allow, deduct, netpay)
        )
        self.conn.commit()
        self.load_table()
        self.reset_form()

    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT name, basic, allowance, deductions, netpay FROM payroll")
        for row in self.cursor.fetchall():
            self.tree.insert("", END, values=row)

    def reset_form(self):
        self.name_var.set("")
        self.basic_var.set(0.0)
        self.allow_var.set(0.0)
        self.deduct_var.set(0.0)
        self.netpay_var.set(0.0)

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = PayrollSystem(root)
    root.mainloop()
