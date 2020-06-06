from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client.mars_db
collection = db.data

@app.route('/')
def home():
    data = collection.find_one()
    return render_template('index.html', mars=data)

# Create route that will trigger scrape functions
@app.route('/scrape')
def scrape():
    mars_info = scrape_mars.scrape()

    # # Insert forecast into database
    collection.drop()
    collection.insert_one(mars_info)
    # Redirect back to home page
    return redirect('/', code=302)



if __name__ == '__main__':
    app.run(debug=True)
    