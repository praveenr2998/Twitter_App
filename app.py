from flask import Flask, request,render_template
from models import features


app = Flask(__name__)

# To insert tweets to DB
@app.route('/')
def hello_world():
    global obj1
    obj1 = features()
    return obj1.insertDataToDb()




if __name__ == '__main__':
	app.run()