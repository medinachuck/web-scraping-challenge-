
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo  

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

@app.route("/scrape")
def scrape():
    mars_web_data = mongo.db.mars_web_data
    scraped_data = scrape_mars.scrape()
    mars_web_data.update({}, scraped_data, upsert=True)
    print('hello')
    return redirect("/", code=302)

@app.route("/")
def index():
    current_info = mongo.db.mars_web_data.find_one()
    return render_template("index.html", current_info = current_info)

if __name__ == "__main__":
    app.run(debug=True)






