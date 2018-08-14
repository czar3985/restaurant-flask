from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, engine


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantMenu.db',  connect_args={'check_same_thread':False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
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
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
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
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('editmenuitem.html', menuItem = menuItem)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):

    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        session.delete(menuItem)
        session.commit()
        flash('Menu item deleted')
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        return render_template('deletemenuitem.html', menuItem = menuItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)