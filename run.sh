docker rm $(docker ps -a -q)
docker build -t app:latest .
# docker run -dp 5000:5000 app
docker run -p 5000:5000 app
