import os
import uuid
import redis
import random
from flask import Flask
from flask import request
from flask import jsonify
from flask import json
import newrelic.agent
newrelic.agent.initialize()

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
#Useful coloUrs
PURPLE = "#800080"
GREEN = "#33CC33"
COLOR = PURPLE

local = True; #Guess the app is running locally
if os.environ.get('VCAP_SERVICES') != None:
    local = False #Corret guess

#Function to get the local IP address
def get_my_ip():
    print "Getting local IP"
    return str(request.environ['REMOTE_ADDR'])

#Return and increment the redis page hitcounter
def count2():
    print "Increasing Count"
    rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
    credentials = rediscloud_service['credentials']
    r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
    number2 = r.incr('HITCOUNT')
    return number2

#Returns a random quote
def buildquotes():
    print "Generating Quote"
    #redis may not be the best choise for this but reasons
    rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
    credentials = rediscloud_service['credentials']
    r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
    if r.get('q1') == None: #See if redis quotes are set, if not initialize
        print "No quotes found, setting"
        r.set('q1', "Don't Panic")
        r.set('q2', "The rest of you keep banging the rocks together")
        r.set('q3', "Time is an illusion, lunchtime doubly so")
        r.set('q4', "Just when you think life can not possibly get any worse it suddenly does")
        r.set('q5', "A common mistake that people make when trying to design something completely foolproof is to underestimate the ingenuity of complete fools")
        r.set('q6', "The ships hung in the sky in much the same way that bricks does not")
        print "Quotes set"
    array1=['q1','q2','q3','q4','q5','q6']
    return str(r.get(random.choice(array1)))

@app.route('/')
def hello():
    #Initial values that will get replaced if on CF, otherwise will not show in HTML
    ip = get_my_ip() #Set IP data
    vistorc2 = "" #Start with blank vistor count
    quote = "" #Start with blank quote
    #Check if we running locally and change string :)
    if str(ip) == "127.0.0.1":
        print "Local environment found"
        ip = "There is no place like 127.0.0.1"
    #Check for CF environment info before running functions that need redis
    if not(local):
        print "CF environment found"
        vistorc2 = "Welcome Vistor Number: " + str(count2()) #Set count
        quote = "'" + buildquotes() + "'" #Set quotes
    return """
    <html>
    <body bgcolor="{}">
    <center>
    <img src="/static/pic1.png" alt="EMware">
    <h1><font color="white">Hi, I'm GUID: <br/>{}
    </br>
    </br>
    Running from: <br/>{}
    </br>
    </br>
    <br/>{}
    </br>
    </br>
    <img src="https://cloudintegration.files.wordpress.com/2011/01/dilbert_cloud_computing.jpg">
    </br>
    </br>
    {}
    </center>

    </body>
    </html>

    """.format(COLOR,my_uuid,ip,vistorc2,quote)

if __name__ == "__main__":
            app.run(threaded=True,debug=local,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
