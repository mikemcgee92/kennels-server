import sqlite3
import json
from models import Location, Employee, Animal

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
  with sqlite3.connect("./kennel.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.address
    FROM location a
    """)
    
    locations = []
    
    dataset = db_cursor.fetchall()
    
    for row in dataset:
      location = Location(row['id'], row['name'], row['address'])
      locations.append(location.__dict__)
  
  return locations

def get_single_location(id):
  with sqlite3.connect("./kennel.sqlite3") as conn:
    conn.row_factory = sqlite3.Row
    db_cursor = conn.cursor()
    
    # Get the location data
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.address
    FROM location a
    WHERE a.id = ?
    """, (id, ))
    
    l_data = db_cursor.fetchone()
    
    # Get the employees matching the location's id
    db_cursor.execute("""
    SELECT
      e.id,
      e.name,
      e.address,
      e.location_id
    FROM employee e
    WHERE e.location_id = ?
    """, (id, ))
    
    employees = []
    e_data = db_cursor.fetchall()
    
    for row in e_data:
      employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
      employees.append(employee.serialized())
    
    # Get the animals matching the location's id
    db_cursor.execute("""
    SELECT
      a.id,
      a.name,
      a.breed,
      a.status,
      a.location_id,
      a.customer_id
    FROM animal a
    WHERE a.location_id = ?
    """, (id, ))
    
    animals = []
    a_data = db_cursor.fetchall()
    
    for row in a_data:
      animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
      animals.append(animal.serialized())
    
    location = Location(l_data['id'], l_data['name'], l_data['address'])
    location.employees = employees
    location.animals = animals
    
  return location.__dict__

def create_location(location):
  max_id = LOCATIONS[-1]["id"]
  new_id = max_id + 1
  location["id"] = new_id
  LOCATIONS.append(location)
  return location

def delete_location(id):
  with sqlite3.connect("./kennel.sqlite3") as conn:
    db_cursor = conn.cursor()
    
    db_cursor.execute("""
    DELETE FROM location
    WHERE id = ?
    """, (id, ))

def update_location(id, new_location):
  for index, location in enumerate(LOCATIONS):
    if location["id"] == id:
      LOCATIONS[index] = new_location
      break
