# build image first
cd app && docker build -t flask_restfulapi:v1 .

# run the container, iteractively so we can see it in action
# notice here I added -e PORT=8080, since we're not using cloud run yet, we need to explicitly 
# specify the PORT environ variable. In cloud run, this is done by google automatically
docker run -it --rm -v "$(pwd):/content" -p 0.0.0.0:8080:8080 -e PORT=8080 flask_restfulapi:v1
