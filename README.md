# RecipeFlask

[RecipeFlask](https://recipes-manager-flask.herokuapp.com/) serves as a storage container for all your recipe links.  Instead of cluttering up your "bookmarks" for your browser and having to sync bookmarks across browsers and devices, let's just create a page where we can nicely store the links to our favorite recipes!

## Features

- See all recipe cards
- Search recipes by keyword, time and cuisine.
- Add a recipe.
- Edit recipes.
- Remove a recipe.
- Add cuisines.
- Edit cuisines.
- Delete cuisines.
- Analytics/Charts

## Getting Started

1. Clone this repository onto your local device.
2. Set up a virtual environment using the `python -m venv .venv` and `source .venv/bin/activate` commands.
3. Update pip in the virtual environment using the `python -m pip install --upgrade pip` command.
4. Install Flask in the virtual environment using the `python -m pip install flask` command.
5. Install dependencies using the `pip install -r requirements.txt` command.
6. Run the app using the `python -m flask run` command.
7. The app will be served at <http://127.0.0.1:5000/> which should be accessible from your browser.

## Dependencies

- Click
- dnspython
- Flask
- Flask-PyMongo
- gunicorn
- itsdangerous
- Jinja2
- MarkupSafe
- pymongo[tls,srv]
- Werkzeug