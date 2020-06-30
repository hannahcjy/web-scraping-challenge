from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_scraping')

@app.route("/")
def home():

    destination_data = mongo.db.collection.find_one()

    return render_template('index_html', mars_data = destination_data )

@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({},mars_data, upsert = True)

    # Redirect back to the home page
    return redirect('/')

if __name__ =='__main__':
    app.run(debug=True)