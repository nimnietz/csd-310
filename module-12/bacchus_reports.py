# Group 5, Milestone 5, CSD310
# William Renard
# Julie Sakai
# Paul Romer
# Tazmin Somerville 

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'bacchus',
    'raise_on_warnings': True,
}

def print_table(headers, data, column_widths=None):
    if column_widths is None:
        column_widths = [max(len(str(row[i])) for row in data + [headers]) for i in range(len(headers))]
    
    header_format = " | ".join(f"{{:{width}}}" for width in column_widths)
    row_format = " | ".join(f"{{:<{width}}}" for width in column_widths)
    
    print(header_format.format(*headers))
    print("-" * (sum(column_widths) + 3 * (len(headers) - 1)))
    
    for row in data:
        print(row_format.format(*[str(item) for item in row]))

def get_late_deliveries():
    cursor.execute(
        "SELECT d.*, s.supplier_name, s.supply_type FROM Delivery d JOIN Supplier s ON d.supplier_id = s.supplier_id;")

    print("\n-- DELIVERY REPORT --")
    print("*This report generates delivery data such as order status and which orders are delayed by how many days.*\n")
    deliveries = cursor.fetchall()

    report_data = []
    for delivery in deliveries:
        delivery_id, supplier_id, expected_date, actual_date, tracking_number, supplier_name, supply_type = delivery
        
        if actual_date is None:
            status = "Pending"
            delay = "N/A"
        else:
            expected = datetime.strptime(str(expected_date), '%Y-%m-%d')
            actual = datetime.strptime(str(actual_date), '%Y-%m-%d')
            difference = actual - expected
            
            if difference.days > 0:
                status = "Delayed"
                delay = f"{difference.days} day(s)"
            else:
                status = "On Time"
                delay = "0 days"

        report_data.append([delivery_id, supplier_name, status, expected_date, actual_date or "N/A", delay])

    headers = ["Delivery ID", "Supplier", "Status", "Expected Date", "Actual Date", "Delay"]
    print_table(headers, report_data)

def get_employee_report():
    cursor.execute(
        "SELECT e.employee_ID, e.employee_first_name, e.employee_last_name, w.hours_worked, w.work_date FROM WorkHours w JOIN Employee e ON w.employee_ID = e.employee_ID ORDER BY w.hours_worked DESC;")

    print("\n-- EMPLOYEE REPORT --")
    print("*This report generates hour data such as how many hours each employee worked for the day \n and which ones are projected to hit overtime and by how much overtime.*\n")
    employee_hours = cursor.fetchall()

    report_data = []
    for employee in employee_hours:
        emp_id, first_name, last_name, hours_worked, work_date = employee
        if hours_worked > 8:
            overtime = hours_worked - 8
            status = f"Overtime: {overtime:.2f} hours"
        else:
            status = "Regular"
        
        report_data.append([emp_id, f"{first_name} {last_name}", work_date, f"{hours_worked:.2f}", status])

    headers = ["Employee ID", "Name", "Date", "Hours Worked", "Status"]
    print_table(headers, report_data)

def get_wine_report():
    cursor.execute(
        "SELECT o.order_id, o.quantity_ordered, w.wine_type, w.wine_name, d.distributor_name FROM `Order` o JOIN Wine w ON o.wine_ID = w.wine_ID JOIN Distributor d ON o.distributor_id = d.distributor_id;")

    print("\n-- WINE PERFORMANCE REPORT --")
    print("*This report generates order data based on wine, wine type, and breaks \n down the total amount of orders based on type of wine carried by Bacchus Winery.*\n")
    
    wine_data = cursor.fetchall()

    report_data = []
    total_red_wine = 0
    total_white_wine = 0
    red_wine_varieties = set()
    white_wine_varieties = set()

    for wine in wine_data:
        order_id, quantity, wine_type, wine_name, distributor = wine
        report_data.append([order_id, wine_name, wine_type, quantity, distributor])
        
        if wine_type == "Red":
            total_red_wine += quantity
            red_wine_varieties.add(wine_name)
        else:
            total_white_wine += quantity
            white_wine_varieties.add(wine_name)

    headers = ["Order ID", "Wine Name", "Type", "Quantity", "Distributor"]
    print_table(headers, report_data)

    print("\n-- TOTAL SALES -- ")
    summary_data = [
        ["Red", total_red_wine, len(red_wine_varieties)],
        ["White", total_white_wine, len(white_wine_varieties)]
    ]
    summary_headers = ["Wine Type", "Total Bottles Sold", "Number of Varieties"]
    print_table(summary_headers, summary_data)

try:
    db = mysql.connector.connect(**config)
    print(f"\n Database user {config['user']} connected to MySQL on host {config['host']} with database {config['database']}")
    input("\n Press any key to generate reports...")

    cursor = db.cursor()

    get_late_deliveries()
    print('\n' * 5)
    get_employee_report()
    print('\n' * 5)
    get_wine_report()
    print('\n' * 5)


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")
    else:
        print(err)
finally:
    db.close()