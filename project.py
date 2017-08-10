from flask import Flask, request, render_template, redirect, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
# binds the engine to the Base class
# makes the connections between class definitions & corresponding tables in db
DBSession = sessionmaker(bind = engine)
# creates sessionmaker object, which establishes link of
# communication between our code executions and the engine we created
session = DBSession()
# create an instance of the DBSession  object - to make a changes
# to the database, we can call a method within the session

@app.route('/')
def indexPage():
    """ Shows a list of restaurants """
    restaurants = session.query(Restaurant).order_by(Restaurant.name)
    return render_template('index.html', restaurants = restaurants)


@app.route('/restaurant/add/', methods=['GET', 'POST'])
def addRestaurant():
    """ Form to add a new restaurant, and logic to POST it to db """
    if request.method == 'POST':
        new_resto = Restaurant(name = request.form['name'])
        session.add(new_resto)
        session.commit()
        flash('Congratulations! Restaurant Successfully Added!')
        return redirect(url_for('indexPage'))
    else:
        return render_template('add_restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    """ Form to delete menu item, and redirect upon POST """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Congratulations! Restaurant Successfully Deleted!')
        return redirect(url_for('indexPage'))
    else:
        return render_template('delete_restaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    """ Form to edit a restaurant name, and logic to POST the edit to db """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        session.query(Restaurant).filter_by(id=restaurant_id).update({"name": request.form['name']})
        session.commit()
        flash('Congratulations! Restaurant Successfully Edited!')
        return redirect(url_for('indexPage'))
    else:
        return render_template('edit_restaurant.html', restaurant = restaurant)


@app.route('/menu/<int:restaurant_id>/')
def menu(restaurant_id):
    """ Shows the menu for a particular restaurant """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/menu/<int:restaurant_id>/newitem/', methods=['GET', 'POST'])
def addMenuItem(restaurant_id):
    """ Form to add a new menu item, and logic to POST the new item to db """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        new_menu_item = MenuItem(name = request.form['item'],
                           description = request.form['description'],
                           price = request.form['price'],
                           restaurant_id = restaurant_id
                           )
        session.add(new_menu_item)
        session.commit()
        flash('Congratulations! Menu Item Successfully Added!')
        return redirect(url_for('menu', restaurant_id = restaurant.id))
    else:
        return render_template('add_menu_item.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    """ Form to delete menu item, and redirect upon POST """
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash('Congratulations! Restaurant Successfully Deleted!')
        return redirect(url_for('menu', restaurant_id = restaurant.id))
    else:
        return render_template('delete_menu_item.html', menu_item = menu_item, restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    """ Form to edit a menu item, and logic to POST updates to db """
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()

    if request.method == 'POST':
        data = ({'name': request.form['name'],
                'description': request.form['description'],
                'price': request.form['price']}
                )
        session.query(MenuItem).filter_by(id=menu_id).update(data)
        session.commit()
        flash('Congratulations! Menu Item Successfully Edited!')
        return redirect(url_for('menu', restaurant_id = restaurant.id))
    else:
        return render_template('edit_menu_item.html', menu_item = menu_item, restaurant = restaurant)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)