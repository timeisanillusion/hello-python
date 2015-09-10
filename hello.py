import os
import uuid
from flask import Flask
from flask import request
from flask import jsonify



app = Flask(__name__)
my_uuid = str(uuid.uuid1())
PURPLE = "#800080"
GREEN = "#33CC33"

COLOR = PURPLE

#Set global value
number = "1"

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return str(request.environ['REMOTE_ADDR'])

#updates the file by 1 when called
def count():
    print "Running function"
    counter = open("counter.txt","r")
    line = counter.readline()
    counter.close()
    number = int(line) + 1
    counter = open("counter.txt","w")
    counter.write(str(number))
    counter.close()
    #Output result on commandline for debug
    return number

@app.route('/')
def hello():
    #Run the function to set the value number and update
    vistorc = count()
    ip = get_my_ip()
    print "Vistor count"
    print str(vistorc)
    print "IP Info"
    print str(ip)
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>
    </br>

    <font color="white">Welcome Vistor Number: <br/>
    {}</br>
    </br>
    <font color="white">Coming from: <br/>{}
    </br>
    </br>
    <img src="https://cloudintegration.files.wordpress.com/2011/01/dilbert_cloud_computing.jpg">
    </center>

    </body>
    </html>


    """.format(COLOR,my_uuid,vistorc,ip)



if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
