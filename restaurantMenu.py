from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantMenu.db',  connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/new/')
def newRestaurant():
    return render_template('newrestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template('editrestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return render_template('deleterestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=menuItems)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def showMenuJSON(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
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
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)


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
        return render_template('editmenuitem.html', menuItem = menuItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('showMenu', restaurant_id = restaurant_id))

    else:
        return render_template('deletemenuitem.html', menuItem = menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)