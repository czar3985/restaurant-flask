from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///restaurantMenu.db',  connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/restaurant/login/')
def showLogin():
	# Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', CLIENT_ID=CLIENT_ID, STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = '<br />'
    flash("You are now logged in as %s" % login_session['username'])
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():

    restaurants = session.query(Restaurant).all()
    if not restaurants:
        flash('There are currently no restaurants in the database.')
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/JSON/')
def showRestaurantsJSON():

    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants = [restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/new/', methods=['GET','POST'])
def newRestaurant():

    if request.method == 'POST':
        newItem = Restaurant(name = request.form['name'])
        session.add(newItem)
        session.commit()
        flash('New restaurant created')
        return redirect(url_for('showRestaurants'))

    else:
        return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'POST':
        if request.form['name'] != '':
            restaurant.name = request.form['name']

        session.add(restaurant)
        session.commit()
        flash('Restaurant edited')
        return redirect(url_for('showRestaurants'))

    else:
        return render_template('editrestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Restaurant deleted')
        return redirect(url_for('showRestaurants'))

    else:
        return render_template('deleterestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    if not menuItems:
        flash('There are currently no menu items for this restaurant.')

    appetizers = []
    entrees = []
    desserts = []
    beverages = []
    for menuItem in menuItems:
        if menuItem.course == 'Appetizer':
            appetizers.append(menuItem)
        elif menuItem.course == 'Entree':
            entrees.append(menuItem)
        elif menuItem.course == 'Dessert':
            desserts.append(menuItem)
        elif menuItem.course == 'Beverage':
            beverages.append(menuItem)

    return render_template('menu.html',
                           restaurant = restaurant,
                           appetizers = appetizers,
                           entrees = entrees,
                           desserts = desserts,
                           beverages = beverages)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showMenuJSON(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [menuItem.serialize for menuItem in menuItems])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def showMenuItemJSON(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem = menuItem.serialize)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],
                           restaurant_id = restaurant_id,
                           price = request.form['price'],
                           description = request.form['description'],
                           course = request.form['course'])
        session.add(newItem)
        session.commit()
        flash('New menu item created')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('newmenuitem.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        if request.form['name'] != '':
            menuItem.name = request.form['name']

        if request.form['price'] != '':
            menuItem.price = request.form['price']

        if request.form['description'] != '':
            menuItem.description = request.form['description']

        menuItem.course = request.form['course']

        session.add(menuItem)
        session.commit()
        flash('Menu item edited')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('editmenuitem.html', restaurantName = restaurant.name, menuItem = menuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('deletemenuitem.html', restaurantName = restaurant.name, menuItem = menuItem)


@app.route('/restaurant/search/', methods=['GET','POST'])
def searchResult():

    if request.method == 'POST':
        search_keyword = request.form['search-keyword']
        search_keyword_lower = search_keyword.lower()

        restaurants_found = []
        restaurants = session.query(Restaurant).all()
        for restaurant in restaurants:
            if search_keyword_lower in restaurant.name.lower():
                restaurants_found.append(restaurant)

        menu_items_found = []
        menuItems = session.query(MenuItem).all()
        for menuItem in menuItems:
            if menuItem.course:
                if search_keyword_lower in menuItem.course.lower():
                    menu_items_found.append(menuItem)
                    continue
            if search_keyword_lower in menuItem.name.lower():
                menu_items_found.append(menuItem)
                continue
            if menuItem.description:
                if search_keyword_lower in menuItem.description.lower():
                    menu_items_found.append(menuItem)

        return render_template('searchresults.html',
                               search_keyword = search_keyword,
                               restaurants_found = restaurants_found,
                               menu_items_found = menu_items_found)

    else:
        return render_template('searchresults.html', search_keyword = '')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)