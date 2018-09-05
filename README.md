# Restaurants

The restaurants application keeps a database of Restaurants and Menu Items for each restaurant.

---

_**This version of the restaurants application uses the Flask framework.**_

## Prerequisites

1. python 2.7.x
2. sqlalchemy
3. sqlite3
4. flask
5. _database_setup.py_
6. _restaurantMenu.py_
7. _lotsofmenus.py_ 
8. Google developers account

## Usage

The following resource gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

_database_setup.py_ will setup the database: _restaurantmenu.db_

_lotsofmenus.py_ will populate the database

_restaurantMenu.py_ will run the web server 

Navigate to port 5000, 

restaurants page: http://localhost:5000/restaurant/

menu page for each restaurant ID in the server PC
Ex: http://localhost:5000/restaurant/1/

Follow the steps below to create _client_secrets.json_

### Google log-in

1. In console.developers.google.com, sign in to your Google account
2. Create Project. Indicate a name for the app
3. Go to your app's page in the Google APIs Console
4. Choose Credentials
5. Create an OAuth Client ID.
6. Configure the consent screen, with email and app name
7. Choose Web application list of application types
8. Set the authorized JavaScript origins - http://localhost:5000
9. Authorized redirect URIs: http://localhost:5000/login and http://localhost:5000/gconnect
10. Download the client secret JSON file and copy the contents to client_secrets.json in the same folder as the restaurant_menu.py file

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

- View restaurants in the database
- Edit a restaurant
- Delete a restaurant
- Add restaurants
- View menu entries for each restaurant in the database
- Create a new menu item for each restaurant
- Update a menu item 
- Delete a menu item from the database
- Search for restaurants or food
- Make use of JSON API endpoints for a list of restaurants, menus for each restaurant and specific menu item

Ex. 

http://localhost:5000/restaurant/JSON, 

http://localhost:5000/restaurant/1/menu/JSON, 

http://localhost:5000/restaurant/1/menu/1/JSON
