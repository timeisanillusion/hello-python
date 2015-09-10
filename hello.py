import os
import uuid
from flask import Flask
import cgi


app = Flask(__name__)
my_uuid = str(uuid.uuid1())
PURPLE = "#800080"
GREEN = "#33CC33"

COLOR = PURPLE

#Set global value
number = "1"

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
    print "count now"
    print str(number)
    return

@app.route('/')
def hello():
    #Run the function to set the value number and update
    count()
    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="white">Hi, I'm GUID:<br/>
    {}</br>

    <center><h1><font color="white">Welcome <br/>
    {}</br>

    </center>

    </body>
    </html>


    """.format(COLOR,my_uuid,number)



if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
