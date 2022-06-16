from flask import Flask, request, jsonify
import pandas as pd
import os 

# define the flask app object
app = Flask(__name__)

###################################################################
# define the endpoints


# example endpoint: http://ralabs.ca/api/v1/test1
@app.route('/api/v1/test1', methods=['GET','POST'])
def test1():

    # grab the incoming json information
    payload = request.json.get("payload")

    # if GET request
    if request.method=='GET':
        return jsonify({ 'msg': 'that was a GET request!', 'this is what you sent me': payload, 'param1': 'sth1', 'param2': 'sth2' })
    
    # if POST request
    elif request.method=='POST':
        return jsonify({ 'msg': 'that was a POST request!', 'this is what you sent me': payload, 'param1': 'sth1', 'param2': 'sth2' })

    # may it is a PUT request or something, which is not supported by this endpoint, so it will return a blank string
    # otherwise it will throw an error to the user, e.g. 'Method Not Allowed' 405.
    # but if we have this empty string, then the server code should be 200 - success, but just empty json
    else:
        return jsonify({})


# you can also do regular string or float returns, not json 
@app.route('/api/v1/test2', methods=['GET','POST'])
def test2():

    # if GET request
    if request.method=='GET':
        return 'this is a string' # <----- string
        
    # if POST request
    elif request.method=='POST':
        return str(123451515.123143) # <------ floats need to be stringified. otherwise it will throw error
        # you can try this by NOT doing str() and see what kind of error you get when pinging this

    # may it is a PUT request or something, which is not supported by this endpoint, so it will return a blank string
    # otherwise it will throw an error to the user, e.g. 'Method Not Allowed' 405.
    # but if we have this empty string, then the server code should be 200 - success, but just empty json
    else:
        return jsonify({})


# send a download (in bytes) for the user, get request
@app.route('/api/v1/downloadfile', methods=['GET'])
def download_file():
    ###################
    # let's assume theres already a file inside the container 
    # creating a CSV file here
    s = open('/content/test.csv','w')
    s.write('1,2,3,4\n4,5,6,6\n')
    s.close()
    ###################
    
    # define the filepath
    output_filepath = f'/content/test.csv'

    # now we read the file into memory, in bytes*, not unicode
    def generate():
        f = open(output_filepath, 'rb')
        ff = f.read()
        os.remove(output_filepath) # <--- notice how we DELETE the file after we read it into memory, since container is going to die anyway, so no point of keeping stuff here
        return ff

    # now we send it to the front 
    r = app.response_class(generate(), mimetype='text/csv')
    r.headers.set('Content-Disposition', 'attachment', filename=output_filepath)
    return r


# RECEIVE an upload (in bytes) from the user, post request
@app.route("/api/v1/uploadfile", methods=['POST'])
def upload_file():

    # we look for the 'file' argument that came from the incoming request
    obj = request.files["file"]

    # grab the filename
    obj_filename = obj.filename

    # save the object to container
    obj.save(obj_filename) # <--- note that you can always change this name with a variable that you pass from the endpoint

    # you can check to see if the file has been saved
    fpath = os.getcwd()+'/'+obj_filename
    print('file located at:', fpath)
    d = pd.read_csv(fpath).to_json(orient="records")
    # you can send any kind of response back
    return jsonify({"result": "uploaded","data":d}), 201


# you can also pass a variable based on the url
# you can set 'defaults' just in case the user does not specify a variable
# here, there is only default for v3, but no default for v1 and v2, 
# ideally, you want the default to start counting from the RIGHT => LEFT. 
@app.route('/api/v1/test5/<string:v1>', defaults={'v1': '11123asdfaf'}, methods=['GET', 'POST'])
@app.route('/api/v1/test5/<string:v1>/<int:v2>/<path:v3>', methods=['GET','POST'])
def test5(v1,v2,v3):
    if request.method=='GET':
        # just to demonstrate this, let's just send back strings
        stuff_to_show = f'v1: {v1}\n\nv2: {v2}\n\nv3: {v3}'
        return stuff_to_show
    else:
        return ''


# boot up the flask server and define params
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

    # notice that we should always use this get PORT or* do 8080. 
    # so that we can run this locally without any issues
    # because for GCP Cloud Run, PORT is automatically defined by Cloud Run, but just in case
    # it does not exist, we still can fill in the blanks by setting it as 8080 without
    # throwing an error
