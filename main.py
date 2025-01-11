import tkinter as tk
from tkinter import ttk, messagebox, END
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
from datetime import datetime
from fpdf import FPDF
import os
import locale

class PDF(FPDF):
    def header(self):
        # Logo (replace 'logo.png' with your logo path)
        # self.image('logo.png', 10, 8, 33)
        
        # Font
        self.set_font('Arial', 'B', 20)
        
        # Title
        self.cell(0, 10, 'Pharmacy Management System', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Font
        self.set_font('Arial', 'I', 8)
        
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

class PharmacyManagementSystem:
    def __init__(self):
        self.root = ttk.Window()
        self.root.title("Pharmacy Management System")
        self.root.geometry("1200x700")
        
        # Set locale for currency formatting
        locale.setlocale(locale.LC_ALL, '')
        
        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pharmacy_db",
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        self.cursor = self.conn.cursor()
        
        # Create tables if they don't exist
        self.create_tables()
        
        # Main UI Components
        self.create_ui()
        
        self.currency = "MAD"
        
    def create_tables(self):
        # Medicines table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                category VARCHAR(50),
                price DECIMAL(10, 2),
                stock INT,
                expiry_date DATE
            )
        ''')
        
        # Sales table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                customer_name VARCHAR(100),
                total_amount DECIMAL(10, 2)
            )
        ''')
        
        # Sale items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sale_id INT,
                medicine_id INT,
                quantity INT,
                price DECIMAL(10, 2),
                FOREIGN KEY (sale_id) REFERENCES sales(id),
                FOREIGN KEY (medicine_id) REFERENCES medicines(id)
            )
        ''')
        self.conn.commit()
        
    def create_ui(self):
        # Title Frame
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=X, padx=10, pady=5)
        
        title_label = ttk.Label(
            title_frame, 
            text="Pharmacy Management System",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=10)
        
        # Main Content Frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Left Frame - Input Form
        input_frame = ttk.LabelFrame(content_frame, text="Medicine Details", padding=15)
        input_frame.pack(side=LEFT, fill=BOTH, expand=False, padx=5, pady=5)
        
        # Input Fields
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.desc_entry = ttk.Text(input_frame, width=30, height=3)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.category_entry = ttk.Entry(input_frame, width=30)
        self.category_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Price:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.price_entry = ttk.Entry(input_frame, width=30)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Stock:").grid(row=4, column=0, padx=5, pady=5, sticky=W)
        self.stock_entry = ttk.Entry(input_frame, width=30)
        self.stock_entry.grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Expiry Date:").grid(row=5, column=0, padx=5, pady=5, sticky=W)
        self.expiry_entry = ttk.DateEntry(input_frame, width=27)
        self.expiry_entry.grid(row=5, column=1, padx=5, pady=5)
        
        # Buttons Frame
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        ttk.Button(
            btn_frame, 
            text="Add", 
            bootstyle="success",
            command=self.add_medicine
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Update",
            bootstyle="warning",
            command=self.update_medicine
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Delete",
            bootstyle="danger",
            command=self.delete_medicine
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Clear",
            bootstyle="secondary",
            command=self.clear_entries
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="New Sale",
            bootstyle="info",
            command=self.create_sales_ui
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Sales Report",
            bootstyle="info",
            command=self.create_sales_report_ui
        ).pack(side=LEFT, padx=5)
        
        # Right Frame - Treeview
        tree_frame = ttk.LabelFrame(content_frame, text="Medicine List", padding=15)
        tree_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        
        # Search Frame
        search_frame = ttk.Frame(tree_frame)
        search_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_medicines)
        
        # Treeview
        columns = ("ID", "Name", "Description", "Category", "Price", "Stock", "Expiry Date")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Load initial data
        self.load_medicines()
        
    def add_medicine(self):
        try:
            name = self.name_entry.get()
            description = self.desc_entry.get("1.0", END).strip()
            category = self.category_entry.get()
            
            # Validation du prix
            try:
                price = float(self.price_entry.get())
                if price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Price must be a valid positive number!")
                return
            
            # Validation du stock
            try:
                stock = int(self.stock_entry.get())
                if stock <= 0:
                    messagebox.showerror("Error", "Stock must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Stock must be a valid positive number!")
                return
            
            # Validation de la date d'expiration
            expiry_date = self.expiry_entry.entry.get()
            day, month, year = expiry_date.split('/')
            expiry = f"{year}-{month}-{day}"
            
            if not all([name, description, category, expiry]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            query = '''INSERT INTO medicines (name, description, category, price, stock, expiry_date)
                      VALUES (%s, %s, %s, %s, %s, %s)'''
            values = (name, description, category, price, stock, expiry)
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            self.clear_entries()
            self.load_medicines()
            messagebox.showinfo("Success", "Medicine added successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding medicine: {str(e)}")
    
    def update_medicine(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a medicine to update!")
                return
            
            medicine_id = self.tree.item(selected_item)['values'][0]
            
            name = self.name_entry.get()
            description = self.desc_entry.get("1.0", END).strip()
            category = self.category_entry.get()
            
            # Validation du prix
            try:
                price = float(self.price_entry.get())
                if price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Price must be a valid positive number!")
                return
            
            # Validation du stock
            try:
                stock = int(self.stock_entry.get())
                if stock <= 0:
                    messagebox.showerror("Error", "Stock must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Stock must be a valid positive number!")
                return
            
            # Validation de la date d'expiration
            expiry_date = self.expiry_entry.entry.get()
            day, month, year = expiry_date.split('/')
            expiry = f"{year}-{month}-{day}"
            
            if not all([name, description, category, expiry]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            query = '''UPDATE medicines 
                      SET name=%s, description=%s, category=%s, price=%s, stock=%s, expiry_date=%s
                      WHERE id=%s'''
            values = (name, description, category, price, stock, expiry, medicine_id)
            
            self.cursor.execute(query, values)
            self.conn.commit()
            
            self.clear_entries()
            self.load_medicines()
            messagebox.showinfo("Success", "Medicine updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error updating medicine: {str(e)}")
    
    def delete_medicine(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select a medicine to delete!")
                return
            
            medicine_id = self.tree.item(selected_item)['values'][0]
            
            # Vérifier si le médicament est utilisé dans des ventes
            check_query = "SELECT COUNT(*) FROM sale_items WHERE medicine_id = %s"
            self.cursor.execute(check_query, (medicine_id,))
            count = self.cursor.fetchone()[0]
            
            if count > 0:
                messagebox.showerror(
                    "Error", 
                    "Cannot delete this medicine because it is used in sales records.\n"
                    "To maintain data integrity, medicines with sales history cannot be deleted."
                )
                return
            
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this medicine?"):
                query = "DELETE FROM medicines WHERE id=%s"
                self.cursor.execute(query, (medicine_id,))
                self.conn.commit()
                
                self.clear_entries()
                self.load_medicines()
                messagebox.showinfo("Success", "Medicine deleted successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting medicine: {str(e)}")
    
    def load_medicines(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = "SELECT * FROM medicines ORDER BY name"
        self.cursor.execute(query)
        medicines = self.cursor.fetchall()
        
        for medicine in medicines:
            self.tree.insert('', END, values=medicine)
    
    def search_medicines(self, event=None):
        search_term = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        query = '''SELECT * FROM medicines 
                  WHERE LOWER(name) LIKE %s 
                  OR LOWER(category) LIKE %s'''
        search_pattern = f'%{search_term}%'
        self.cursor.execute(query, (search_pattern, search_pattern))
        
        medicines = self.cursor.fetchall()
        for medicine in medicines:
            self.tree.insert('', END, values=medicine)
    
    def item_selected(self, event=None):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            
            self.clear_entries()
            
            self.name_entry.insert(0, values[1])
            self.desc_entry.insert("1.0", values[2])
            self.category_entry.insert(0, values[3])
            self.price_entry.insert(0, values[4])
            self.stock_entry.insert(0, values[5])
            
            # Convert date from YYYY-MM-DD to DD/MM/YYYY format for DateEntry
            date_str = str(values[6])
            year, month, day = date_str.split('-')
            self.expiry_entry.entry.delete(0, END)
            self.expiry_entry.entry.insert(0, f"{day}/{month}/{year}")
    
    def clear_entries(self):
        self.name_entry.delete(0, END)
        self.desc_entry.delete("1.0", END)
        self.category_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.stock_entry.delete(0, END)
        self.expiry_entry.entry.delete(0, END)
    
    def sort_treeview(self, col):
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        items.sort()
        
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def create_sales_ui(self):
        # Sales Window
        self.sales_window = ttk.Toplevel(self.root)
        self.sales_window.title("New Sale")
        self.sales_window.geometry("800x600")
        
        # Customer Details Frame
        customer_frame = ttk.LabelFrame(self.sales_window, text="Customer Details", padding=15)
        customer_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Label(customer_frame, text="Customer Name:").pack(side=LEFT, padx=5)
        self.customer_name_entry = ttk.Entry(customer_frame, width=30)
        self.customer_name_entry.pack(side=LEFT, padx=5)
        
        # Cart Frame
        cart_frame = ttk.LabelFrame(self.sales_window, text="Shopping Cart", padding=15)
        cart_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Add Item Frame
        add_item_frame = ttk.Frame(cart_frame)
        add_item_frame.pack(fill=X, pady=5)
        
        ttk.Label(add_item_frame, text="Medicine:").pack(side=LEFT, padx=5)
        self.sale_medicine_var = ttk.StringVar()
        self.sale_medicine_combo = ttk.Combobox(add_item_frame, textvariable=self.sale_medicine_var, width=30)
        self.sale_medicine_combo.pack(side=LEFT, padx=5)
        
        ttk.Label(add_item_frame, text="Quantity:").pack(side=LEFT, padx=5)
        self.sale_quantity_entry = ttk.Entry(add_item_frame, width=10)
        self.sale_quantity_entry.pack(side=LEFT, padx=5)
        
        ttk.Button(
            add_item_frame,
            text="Add to Cart",
            bootstyle="success",
            command=self.add_to_cart
        ).pack(side=LEFT, padx=5)
        
        # Cart Treeview
        columns = ("ID", "Medicine", "Quantity", "Price", "Total")
        self.cart_tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, width=100)
        
        self.cart_tree.pack(fill=BOTH, expand=True, pady=5)
        
        # Total Frame
        total_frame = ttk.Frame(cart_frame)
        total_frame.pack(fill=X, pady=5)
        
        self.total_label = ttk.Label(total_frame, text="Total: 0.00 MAD", font=("Helvetica", 12, "bold"))
        self.total_label.pack(side=RIGHT, padx=5)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.sales_window)
        btn_frame.pack(fill=X, padx=10, pady=5)
        
        ttk.Button(
            btn_frame,
            text="Complete Sale",
            bootstyle="success",
            command=self.complete_sale
        ).pack(side=RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Cancel",
            bootstyle="danger",
            command=self.sales_window.destroy
        ).pack(side=RIGHT, padx=5)
        
        # Load medicines into combobox
        self.load_medicines_for_sale()

    def generate_invoice(self, sale_id):
        try:
            # Get sale information
            query = "SELECT * FROM sales WHERE id = %s"
            self.cursor.execute(query, (sale_id,))
            sale = self.cursor.fetchone()
            
            # Get sale items
            query = """
                SELECT m.name, si.quantity, si.price, (si.quantity * si.price) as total
                FROM sale_items si
                JOIN medicines m ON si.medicine_id = m.id
                WHERE si.sale_id = %s
            """
            self.cursor.execute(query, (sale_id,))
            items = self.cursor.fetchall()
            
            # Create PDF
            pdf = PDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Invoice Header
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, f'Invoice #{sale_id}', 0, 1, 'L')
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Date: {sale[1]}', 0, 1, 'L')
            pdf.cell(0, 10, f'Customer: {sale[2]}', 0, 1, 'L')
            pdf.ln(10)
            
            # Table Header
            pdf.set_fill_color(200, 200, 200)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(80, 10, 'Medicine', 1, 0, 'C', True)
            pdf.cell(30, 10, 'Quantity', 1, 0, 'C', True)
            pdf.cell(40, 10, 'Price', 1, 0, 'C', True)
            pdf.cell(40, 10, 'Total', 1, 1, 'C', True)
            
            # Table Content
            pdf.set_font('Arial', '', 12)
            for item in items:
                pdf.cell(80, 10, str(item[0]), 1, 0, 'L')
                pdf.cell(30, 10, str(item[1]), 1, 0, 'C')
                pdf.cell(40, 10, f'{item[2]:.2f} {self.currency}', 1, 0, 'R')
                pdf.cell(40, 10, f'{item[3]:.2f} {self.currency}', 1, 1, 'R')
            
            # Total
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(150, 10, 'Total:', 1, 0, 'R')
            pdf.cell(40, 10, f'{sale[3]:.2f} {self.currency}', 1, 1, 'R')
            
            # Save PDF
            filename = f"invoice_{sale_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            
            # Open PDF
            os.startfile(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating invoice: {str(e)}")

    def load_medicines_for_sale(self):
        query = "SELECT id, name, price FROM medicines WHERE stock > 0"
        self.cursor.execute(query)
        self.available_medicines = {f"{row[1]} (${row[2]})": row for row in self.cursor.fetchall()}
        self.sale_medicine_combo['values'] = list(self.available_medicines.keys())

    def add_to_cart(self):
        try:
            selected_medicine = self.sale_medicine_var.get()
            quantity = int(self.sale_quantity_entry.get())
            
            if not selected_medicine or quantity <= 0:
                messagebox.showerror("Error", "Please select a medicine and enter a valid quantity")
                return
            
            medicine_id, name, price = self.available_medicines[selected_medicine]
            
            # Check stock
            query = "SELECT stock FROM medicines WHERE id = %s"
            self.cursor.execute(query, (medicine_id,))
            available_stock = self.cursor.fetchone()[0]
            
            if quantity > available_stock:
                messagebox.showerror("Error", f"Only {available_stock} units available in stock")
                return
            
            total = price * quantity
            
            # Add to cart treeview
            self.cart_tree.insert('', END, values=(medicine_id, name, quantity, price, total))
            
            # Update total
            self.update_cart_total()
            
            # Clear entries
            self.sale_medicine_var.set('')
            self.sale_quantity_entry.delete(0, END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error adding to cart: {str(e)}")

    def update_cart_total(self):
        total = sum(float(self.cart_tree.item(item)['values'][4]) for item in self.cart_tree.get_children())
        self.total_label.config(text=f"Total: {total:.2f} {self.currency}")

    def complete_sale(self):
        try:
            if not self.cart_tree.get_children():
                messagebox.showerror("Error", "Cart is empty!")
                return
            
            customer_name = self.customer_name_entry.get()
            if not customer_name:
                messagebox.showerror("Error", "Please enter customer name!")
                return
            
            # Calculate total
            total_amount = sum(float(self.cart_tree.item(item)['values'][4]) 
                             for item in self.cart_tree.get_children())
            
            # Insert sale record
            query = "INSERT INTO sales (customer_name, total_amount) VALUES (%s, %s)"
            self.cursor.execute(query, (customer_name, total_amount))
            self.conn.commit()
            sale_id = self.cursor.lastrowid
            
            # Insert sale items and update stock
            for item in self.cart_tree.get_children():
                values = self.cart_tree.item(item)['values']
                medicine_id, quantity = values[0], values[2]
                price = values[3]
                
                # Insert sale item
                query = "INSERT INTO sale_items (sale_id, medicine_id, quantity, price) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(query, (sale_id, medicine_id, quantity, price))
                
                # Update stock
                query = "UPDATE medicines SET stock = stock - %s WHERE id = %s"
                self.cursor.execute(query, (quantity, medicine_id))
            
            self.conn.commit()
            
            # Generate and print invoice
            self.generate_invoice(sale_id)
            
            messagebox.showinfo("Success", "Sale completed successfully!")
            self.sales_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error completing sale: {str(e)}")

    def create_sales_report_ui(self):
        # Sales Report Window
        self.report_window = ttk.Toplevel(self.root)
        self.report_window.title("Sales Report")
        self.report_window.geometry("1000x600")
        
        # Filter Frame
        filter_frame = ttk.LabelFrame(self.report_window, text="Filter Options", padding=15)
        filter_frame.pack(fill=X, padx=10, pady=5)
        
        # Date Filter
        ttk.Label(filter_frame, text="From:").pack(side=LEFT, padx=5)
        self.date_from = ttk.DateEntry(filter_frame)
        self.date_from.pack(side=LEFT, padx=5)
        
        ttk.Label(filter_frame, text="To:").pack(side=LEFT, padx=5)
        self.date_to = ttk.DateEntry(filter_frame)
        self.date_to.pack(side=LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Apply Filter",
            bootstyle="primary",
            command=self.filter_sales
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Print Report",
            bootstyle="success",
            command=self.print_sales_report
        ).pack(side=LEFT, padx=5)
        
        # Sales Treeview
        tree_frame = ttk.Frame(self.report_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        columns = ("ID", "Date", "Customer", "Items", "Total Amount")
        self.sales_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        for col in columns:
            self.sales_tree.heading(col, text=col, command=lambda c=col: self.sort_sales_treeview(c))
            self.sales_tree.column(col, width=150)
        
        self.sales_tree.pack(side=LEFT, fill=BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.sales_tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        # Double click to view invoice
        self.sales_tree.bind('<Double-1>', self.view_sale_invoice)
        
        # Load initial sales data
        self.load_sales()

    def load_sales(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        query = """
            SELECT s.id, s.date, s.customer_name, 
                   COUNT(si.id) as item_count, 
                   s.total_amount
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            GROUP BY s.id
            ORDER BY s.date DESC
        """
        self.cursor.execute(query)
        sales = self.cursor.fetchall()
        
        for sale in sales:
            # Format the date
            formatted_date = sale[1].strftime('%Y-%m-%d %H:%M:%S')
            # Format the total with currency
            formatted_total = f"{sale[4]:.2f} {self.currency}"
            values = (sale[0], formatted_date, sale[2], sale[3], formatted_total)
            self.sales_tree.insert('', END, values=values)

    def filter_sales(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Convert dates from DD/MM/YYYY to YYYY-MM-DD format
        from_date = self.convert_date_format(self.date_from.entry.get())
        to_date = self.convert_date_format(self.date_to.entry.get())
        
        query = """
            SELECT s.id, s.date, s.customer_name, 
                   COUNT(si.id) as item_count, 
                   s.total_amount
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            WHERE DATE(s.date) BETWEEN %s AND %s
            GROUP BY s.id
            ORDER BY s.date DESC
        """
        self.cursor.execute(query, (from_date, to_date))
        sales = self.cursor.fetchall()
        
        for sale in sales:
            formatted_date = sale[1].strftime('%Y-%m-%d %H:%M:%S')
            formatted_total = f"{sale[4]:.2f} {self.currency}"
            values = (sale[0], formatted_date, sale[2], sale[3], formatted_total)
            self.sales_tree.insert('', END, values=values)

    def print_sales_report(self):
        try:
            # Get filtered sales
            sales = []
            for item in self.sales_tree.get_children():
                sales.append(self.sales_tree.item(item)['values'])
            
            if not sales:
                messagebox.showwarning("Warning", "No sales to print!")
                return
            
            # Create PDF
            pdf = PDF()
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Sales Report', 0, 1, 'C')
            
            # Date Range
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'From: {self.date_from.entry.get()} To: {self.date_to.entry.get()}', 0, 1, 'C')
            pdf.ln(10)
            
            # Table Header
            pdf.set_fill_color(200, 200, 200)
            pdf.set_font('Arial', 'B', 12)
            headers = ['ID', 'Date', 'Customer', 'Items', 'Total']
            col_widths = [20, 40, 50, 30, 40]
            
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 10, header, 1, 0, 'C', True)
            pdf.ln()
            
            # Table Content
            pdf.set_font('Arial', '', 12)
            total_amount = 0
            
            for sale in sales:
                pdf.cell(col_widths[0], 10, str(sale[0]), 1, 0, 'C')
                pdf.cell(col_widths[1], 10, str(sale[1]), 1, 0, 'C')
                pdf.cell(col_widths[2], 10, str(sale[2]), 1, 0, 'L')
                pdf.cell(col_widths[3], 10, str(sale[3]), 1, 0, 'C')
                pdf.cell(col_widths[4], 10, str(sale[4]), 1, 0, 'R')
                pdf.ln()
                
                # Add to total (remove currency symbol for calculation)
                total_amount += float(str(sale[4]).replace(self.currency, '').strip())
            
            # Total
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(sum(col_widths[:-1]), 10, 'Total:', 1, 0, 'R')
            pdf.cell(col_widths[-1], 10, f'{total_amount:.2f} {self.currency}', 1, 1, 'R')
            
            # Save PDF
            filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf.output(filename)
            
            # Open PDF
            os.startfile(filename)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error generating report: {str(e)}")

    def convert_date_format(self, date_str):
        day, month, year = date_str.split('/')
        return f"{year}-{month}-{day}"

    def view_sale_invoice(self, event):
        selected_item = self.sales_tree.selection()
        if selected_item:
            sale_id = self.sales_tree.item(selected_item)['values'][0]
            self.generate_invoice(sale_id)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PharmacyManagementSystem()
    app.run()
