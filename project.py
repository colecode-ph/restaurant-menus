from flask import Flask
app = Flask(__name__)

from flask import request, render_template, redirect, url_for

from sqlalchemy import create_engine, func, update
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
# lets the program know which database we want to query
Base.metadata.bind = engine
# binds the engine to the Base class -
# this makes the connections between our class definitions
# and the corresponding tables in the database
DBSession = sessionmaker(bind = engine)
# creates a sessionmaker object, which establishes a link of
# communication between our code executions and the engine we created
session = DBSession()
# create an instance of the DBSession  object - to make a changes
# to the database, we can call a method within the session

@app.route('/')
def IndexPage():
    """ Shows a list of restaurants """
    restaurants = session.query(Restaurant).order_by(Restaurant.name)
    return render_template('index.html', restaurants = restaurants)


@app.route('/menu/<int:restaurant_id>')
def Menu(restaurant_id):
    """ Shows the menu for a particular restaurant """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)


@app.route('/menu/<int:restaurant_id>/newitem', methods=['GET', 'POST'])
def NewItem(restaurant_id):
    """ Form to add a new menu item, and logic to POST the new item to db """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        newItem = MenuItem(name = request.form['item'],
                           description = request.form['description'],
                           price = request.form['price'],
                           restaurant_id = restaurant_id
                           )
        session.add(newItem)
        session.commit()
        return redirect(url_for('Menu', restaurant_id = restaurant.id))

    else:
        return render_template('menu_item.html', restaurant = restaurant)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    """ Form to edit a menu item """
    # restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    # menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    return "page to edit a menu item. Task 2 complete!"



@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    # return "page to delete a menu item. Task 3 complete!"
    menu_item = session.query(MenuItem).filter_by(id = menu_id).one()
    output = "are you sure you want to delete {}?".format(menu_item.name)
    return output


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)