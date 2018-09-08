from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine

from flask import session as login_session
import random, string


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantMenu.db',  connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/restaurant/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_letters + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


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