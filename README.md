# Restaurants

The restaurants application keeps a database of Restaurants and Menu Items for each restaurant.

---

_**This version of the restaurants application uses the Flask framework.**_

## Prerequisites

1. python 2.7.x
2. sqlalchemy
3. sqlite3
4. flask
5. _database_setup.py_ from the github repository [restaurants](https://github.com/czar3985/restaurants-flask)
5. _restaurantMenu.py_ from the same restaurant-flask repository

## Usage

The following resource gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

_database_setup.py_ will setup the database: _restaurantmenu.db_

_restaurantMenu.py_ will run the web server 

Navigate to port 8080, menu page for each restaurant ID in the server PC
Ex: http://SERVERPC:5000/restaurants/1/menu

## Database Structure

```
Table Name: restaurant
Columns:
{'primary_key': 0, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'name'}
{'primary_key': 1, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'id'}

Table Name: menu_item
Columns:
{'primary_key': 0, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=80), 'name': u'name'}
{'primary_key': 1, 'nullable': False, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'id'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'description'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=8), 'name': u'price'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': VARCHAR(length=250), 'name': u'course'}
{'primary_key': 0, 'nullable': True, 'default': None, 'autoincrement': 'auto', 'type': INTEGER(), 'name': u'restaurant_id'}
```

## Features

- View menu entries for each restaurant in the database
- Create a new menu item for each restaurant
- Update a menu item 
- Delete a menu item from the database
- Provides a JSON API endpoint for each restaurant:
http://SERVERPC:5000/restaurants/1/menu/JSON

## To Dos

- Update HTML and CSS to make it my own
- CRUD operations for restaurants
- Login and authentication

## Acknowledgement

Coded while following along the Flask framework tutorial of Full Stack Foundations by Udacity.
_styles.css_ is unmodified from the tutorial.