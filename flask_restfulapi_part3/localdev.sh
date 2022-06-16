cd app && docker run -it --rm -v "$(pwd):/content" -p 0.0.0.0:8080:8080 python:3.8 bash
pip install Flask requests pandas numpy
cd /content/src
python server.py 