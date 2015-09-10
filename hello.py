import os
import uuid
import redis
import random
from flask import Flask
from flask import request
from flask import jsonify
from flask import json

#servicedataexport  = json.dumps(rediscloud)


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
PURPLE = "#800080"
GREEN = "#33CC33"

COLOR = PURPLE

#Set global value
#number = "1"
#number2 = "1"

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return str(request.environ['REMOTE_ADDR'])

#updates the file by 1 when called
#def count():
#    print "Running function"
#    counter = open("counter.txt","r")
#    line = counter.readline()
#    counter.close()
#    number = int(line) + 1
#    counter = open("counter.txt","w")
#    counter.write(str(number))
#    counter.close()
    #Output result on commandline for debug
#    return number

def count2():
    rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
    credentials = rediscloud_service['credentials']
    r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
    r.incr('HITCOUNT')
    number2 = r.get('HITCOUNT')

    return number2


def buildquotes():
    rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
    credentials = rediscloud_service['credentials']
    r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])
    r.set('q1', "Don't Panic")
    r.set('q2', "The rest of you keep banging the rocks together")
    r.set('q3', "Time is an illusion, lunchtime doubly so")
    r.set('q4', "Just when you think life can not possibly get any worse it suddenly does")
    r.set('q5', "A common mistake that people make when trying to design something completely foolproof is to underestimate the ingenuity of complete fools")
    r.set('q6', "The ships hung in the sky in much the same way that bricks does not")

    array1=['q1','q2','q3','q4','q5','q6']

    return str(r.get(random.choice(array1)))

@app.route('/')
def hello():
    #Run the function to set the value number and update
#    vistorc = count()
    vistorc2 = count2()
    ip = get_my_ip()
    print "Vistor count"
    print str(vistorc2)
    print "IP Info"
    print str(ip)
    quote = buildquotes()
    print str(quote)
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>
    </br>
    <font color="white">Running from: <br/>
    {}</br>
    </br>
    <font color="white">Welcome Vistor Number (redis): <br/>{}
    </br>
    <img src="https://cloudintegration.files.wordpress.com/2011/01/dilbert_cloud_computing.jpg">
    </br>
    {}
    </center>



    </body>
    </html>


    """.format(COLOR,my_uuid,ip,vistorc2,quote)



if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
