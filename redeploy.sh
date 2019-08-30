docker build --tag=flaskdock3 .
docker tag flaskdock3 runwith/get-started:flask
docker push runwith/get-started:flask
docker stack deploy -c docker-compose.yml flack