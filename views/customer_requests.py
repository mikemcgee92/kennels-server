import sqlite3
import json
from models import Customer

CUSTOMERS = [
  {
    "id": 1,
    "name": "Ryan Tanay"
  }
]

def get_all_customers():
  with sqlite3.connect("./kennel.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.address,
      a.email,
      a.password
    FROM customer a
    """)
    
    customers = []
    
    dataset = db_cursor.fetchall()
    
    for row in dataset:
      customer = Customer(row['id'], row['name'], row['address'],
                          row['email'], row['password'])
      customers.append(customer.__dict__)
  
  return customers

def get_single_customer(id):
  with sqlite3.connect("./kennel.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.address,
      a.email,
      a.password
    FROM customer a
    WHERE a.id = ?
    """, (id, ))
    
    data = db_cursor.fetchone()
    
    customer = Customer(data['id'], data['name'], data['address'],
                        data['email'], data['password'])
    
  return customer.__dict__

def create_customer(customer):
  max_id = CUSTOMERS[-1]["id"]
  new_id = max_id + 1
  customer["id"] = new_id
  CUSTOMERS.append(customer)
  return customer

def delete_customer(id):
  customer_index = -1
  
  for index, customer in enumerate(CUSTOMERS):
    if customer["id"] == id:
      customer_index = index
  
  if customer_index >= 0:
    CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
  for index, customer in enumerate(CUSTOMERS):
    if customer["id"] == id:
      CUSTOMERS[index] = new_customer
      break
