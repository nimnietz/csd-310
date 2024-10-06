# Group 5, Milestone 3, CSD310
# William Renard
# Julie Sakai
# Paul Romer
# Tazmin Somerville 

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

config = {
    'user': 'root',
    'password': 'YOUR PASSWORD',
    'host': '127.0.0.1',
    'database': 'bacchus',
    'raise_on_warnings': True,
}


def get_late_deliveries():
    cursor.execute(
        "SELECT d.*, s.supplier_name, s.supply_type FROM delivery d JOIN supplier s ON d.supplier_id = s.supplier_id ORDER BY d.delivery_status;")

    print("\n-- DELIVERY REPORT --")
    print("*This report generates delivery data such as order status and which orders are delayed by how many days.*\n")
    late_deliveries = cursor.fetchall()

    # length is 8
    for delivery in late_deliveries:
        if delivery[4] == "Delayed":
            actual_date = datetime.strptime(str(delivery[3]), '%Y-%m-%d')
            expected_date = datetime.strptime(str(delivery[2]), '%Y-%m-%d')
            difference = actual_date - expected_date
            print("[{}] Delivery from: {} | {} Day(s) Late".format(delivery[4], delivery[6], str(difference.days)))
        else:
            print("[{}] Delivery from: {}".format(delivery[4], delivery[6]))


def get_employee_report():
    cursor.execute(
        "SELECT e.employee_ID, e.employee_first_name, w.hours_worked FROM workhours w JOIN employee e ON w.employee_ID = e.employee_ID ORDER BY w.hours_worked DESC;")

    print("\n-- EMPLOYEE REPORT --")
    print(
        "*This report generates hour data such as how many hours each employee worked for the day and which ones are \n projected to hit overtime and by how much overtime.*\n")
    employee_hours = cursor.fetchall()

    for employee in employee_hours:
        if employee[2] > 8:
            projection = employee[2] - 8
            print("Employee: {} [ID: {}] Hours Worked: {} | Projected Overtime: {}".format(employee[1], employee[0],
                                                                                           employee[2], projection))
        else:
            print("Employee: {} [ID: {}] Hours Worked: {}".format(employee[1], employee[0], employee[2]))


def get_wine_report():
    cursor.execute(
        "SELECT o.order_id, o.quantity_ordered, w.wine_type, w.wine_name, d.distributor_name FROM `order` o JOIN `wine` w ON o.wine_ID = w.wine_ID JOIN `distributor` d ON o.distributor_id = d.distributor_id;")

    print("\n-- WINE PERFORMANCE REPORT --")
    print("*This report generates order data based on wine, wine type, and breaks down the total amount of orders based \n on type of wine carried by Bacchus Winery.*")
    total_red_wine = 0
    total_white_wine = 0
    red_wine_varieties = 0
    white_wine_varieties = 0

    wine_data = cursor.fetchall()

    for wine in wine_data:
        if wine[2] == "Red":
            total_red_wine += int(wine[1])
            red_wine_varieties += 1
        else:
            total_white_wine += int(wine[1])
            white_wine_varieties += 1
        print("Wine: {} [{}] | Amount Ordered: {} by Distributor: {}".format(wine[3], wine[2], wine[1], wine[4]))

    print("\n-- TOTAL SALES -- ")
    print("Sold {} Red bottles of wine in {} variation(s).".format(total_red_wine, red_wine_varieties))
    print("Sold {} White bottles of wine in {} variation(s).".format(total_white_wine, white_wine_varieties))

try:
    db = mysql.connector.connect(**config)
    print("\n Database user {} connected to MySQL on host {} with database {}".format(config['user'], config['host'],
                                                                                      config['database']))
    input("\n Press any key to generate reports...")

    cursor = db.cursor()

    get_late_deliveries()
    get_employee_report()
    get_wine_report()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("   The specified database does not exist")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("   The specified database does not exist")
    else:
        print(err)
finally:
    db.close()
