'''
This is a set of snippets to test the restful api

# no need to expose port for this testing container

docker run -it --rm python:3.8 bash 
pip install requests
mkdir /content
cd /content
python 

# then you're good to go




'''


#######################################################################################
# test1 - simple GET and POST in json 
import requests 

# define json payload
payload = {'payload':'hey'}


# GET request
# send in there request 
r = requests.get('https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test1', json=payload)
# check output 
r.json()


# POST request
r = requests.post('https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test1', json=payload)
# check output 
r.json()




#######################################################################################
# test2 - GET and POST, but its numbers and strings

# define json payload
payload = {'payload':'hey'}


# GET request
# send in there request 
r = requests.get('https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test2', json=payload)
# check output (notice it is NOT json() anymore. just r.text)
r.text


# POST request
r = requests.post('https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test2', json=payload)
# check output 
r.text
# notice it is a stringified version of a float




#######################################################################################
# test3 - download a file and save to disk
# you have to know the file extension of the file. so in this case, we know it is 
# a CSV file, so we save as *.csv. 

# grab the file, streamed
r = requests.get('https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/downloadfile', stream=True) # <--- notice the stream

# chunk it when we download to reduce load in memory
chunk_size = 2000 # how many bytes you want to download at a time
with open('/content/output.csv', 'wb') as fd:
    for chunk in r.iter_content(chunk_size):
        fd.write(chunk)












#######################################################################################
# test4 - upload a file to the server
import os

# let's just create sth first
s = open('/content/file2upload.csv','w')
s.write('1,2,3,4\n4,5,6,6\n')
s.close()

file = '/content/file2upload.csv' # file on local disk containing Dockerfile and other files

# send in the post request. This will send upload the file to the manager node,
# which will in turn upload it to the bucket
r = requests.post(
    'https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/uploadfile', 
    files={
        'file': (os.path.basename(file), open(file, 'rb'), 'application/octet-stream')
    }
)

# check response
r.json()



#######################################################################################
# test5
# can also do it in browser:
# https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test5/myv1/213414151/myv////135151!@$?!@$!?$
r = requests.get(
    'https://flask-restfulapi-test1-v2he6t5deq-uw.a.run.app/api/v1/test5/myv1/213414151/myv////135151!@$?!@$!?$'
)

# check response
r.text