# Pharmacy Management System

A comprehensive desktop application for managing pharmacy operations, built with Python and ttkbootstrap. This system helps pharmacies manage their inventory, process sales, and generate reports efficiently.

## Features

- **Inventory Management**
  - Add, update, and delete medicines
  - Track stock levels
  - Monitor expiry dates
  - Search and filter medicines
  - Sort by various parameters

- **Sales Management**
  - Process sales transactions
  - Generate invoices automatically
  - Track customer information
  - Real-time stock updates

- **Reporting System**
  - Generate sales reports
  - Filter sales by date range
  - Export reports to PDF
  - View transaction history

- **User-Friendly Interface**
  - Modern and intuitive design
  - Responsive layout
  - Easy navigation
  - Form validation

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- MySQL Server
- Required Python packages:
  ```
  tkinter
  ttkbootstrap
  mysql-connector-python
  fpdf
  ```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pharmacy-management-system.git
   cd pharmacy-management-system
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL database:
   - Create a new database named `pharmacy_db`
   - Configure the database connection in `PharmacyManagementSystem.__init__`:
     ```python
     self.conn = mysql.connector.connect(
         host="localhost",
         user="your_username",
         password="your_password",
         database="pharmacy_db",
         charset="utf8mb4",
         collation="utf8mb4_general_ci"
     )
     ```

4. Run the application:
   ```bash
   python main.py
   ```

## Database Structure

The system uses three main tables:

1. **medicines**
   - id (Primary Key)
   - name
   - description
   - category
   - price
   - stock
   - expiry_date

2. **sales**
   - id (Primary Key)
   - date
   - customer_name
   - total_amount

3. **sale_items**
   - id (Primary Key)
   - sale_id (Foreign Key)
   - medicine_id (Foreign Key)
   - quantity
   - price

## Usage

### Managing Medicines

1. Add new medicines using the input form
2. Update existing medicines by selecting them from the list
3. Delete medicines that are no longer sold
4. Search medicines by name or category

### Processing Sales

1. Click "New Sale" to open the sales window
2. Enter customer information
3. Add items to the cart
4. Complete the sale to generate an invoice

### Generating Reports

1. Click "Sales Report" to open the reporting interface
2. Set date range for filtering
3. View sales history
4. Generate PDF reports
5. Double-click on any sale to view its invoice

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please create an issue in the GitHub repository or contact [your-email@example.com].

## Acknowledgments

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) for the modern UI components
- [FPDF](http://www.fpdf.org/) for PDF generation capabilities
- All contributors who participate in this project

## Screenshots

(Add screenshots of your application here)

## Future Improvements

- User authentication system
- Multiple user roles (Admin, Cashier, etc.)
- Backup and restore functionality
- Email integration for invoices
- Barcode scanner integration
- Mobile application integration
