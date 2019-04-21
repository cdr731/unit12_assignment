# Unit 12 Assignment - Mission to Mars
# by Christopher Reutz

# Dependencies
from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Import the Mars scraping code
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to Mars database. Will create one if not already available.
db = client.mission_to_mars_db

# Route to query Mongo database and pass data to html template
@app.route("/")
def home():
	mars_fields = db.mars_collection.find_one()
	return render_template("index.html", mars_fields=mars_fields)

# Route to scrape data
@app.route("/scrape")
def scrape():
	mars_data = scrape_mars.scrape()
	db.mars_collection.update({}, mars_data, upsert=True)
	return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)