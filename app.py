import os 
import re
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
from flask import jsonify

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'RecipeFlask'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tuser@recipeflask.ftovt.mongodb.net/RecipeFlask?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -----Homepage------

@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    if (request.args.get('recipe_name') is not None 
    or request.args.get('preparation_time') is not None 
    or request.args.get('category_name') is not None):
        recipename = None
        preparationtime = None
        categoryname = None
        
        if request.args.get('recipe_name') is not None and request.args.get('recipe_name') is not '':
            recipenameregex = "\W*"+request.args.get("recipe_name")+"\W*"
            recipename = re.compile(recipenameregex, re.IGNORECASE)
          
        if request.args.get('preparation_time') is not None and request.args.get('preparation_time') is not '':
            preparationtimeregex = "\W*"+request.args.get("preparation_time")+"\W*"
            preparationtime = re.compile(preparationtimeregex, re.IGNORECASE)
        
        if request.args.get('category_name') is not None and request.args.get('category_name') is not '':
            categoryregex = "\W*"+request.args.get("category_name")+"\W*"
            categoryname = re.compile(categoryregex, re.IGNORECASE)
            

        recipes=mongo.db.recipes.find( { "$or": [{"recipe_name": recipename}, {"preparation_time": preparationtime}, {"category_name": categoryname}] } )
        return render_template("recipes.html", recipes=recipes, categories=mongo.db.categories.find()) 
        
    return render_template("recipes.html", recipes=mongo.db.recipes.find(), categories=mongo.db.categories.find())
    
    

# -----Charts------
@app.route('/charts')
def charts():
    results = {"labels": [ ], "data": [ ]}
    categories = mongo.db.categories
    recipes = mongo.db.recipes
    all_categories = categories.find({})
    for category in all_categories:
        category_counts = recipes.find({"category_name": category["category_name"]}).count()
        results["labels"].append(category["category_name"])
        results["data"].append(category_counts)
    
    return render_template("charts.html", results=results)
    
    
# -----Add Recipe------
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           categories=mongo.db.categories.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


# -----Edit Recipe------

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe,
                           categories=all_categories)


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'category_name':request.form.get('category_name'),
        'recipe_intro':request.form.get('recipe_intro'),
        'ingredients': request.form.get('ingredients'),
        'description': request.form.get('description'),
        'preparation_time': request.form.get('preparation_time'),
        'photo_url': request.form.get('photo_url')
        
    })
    return redirect(url_for('get_recipes'))


# -----Delete Recipe------

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


# -----Categories funcitionalities------

@app.route('/categories')
def categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())
                           
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))                           

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('categories'))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('categories'))

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')
   
    
# -----Single Page Recipe------

@app.route('/recipe_single/<recipe_id>')
def recipe_single(recipe_id):
    return render_template("recipepage.html",
                           recipes=mongo.db.recipes.find({'_id': ObjectId(recipe_id)}))
                           

# ************************************************

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
