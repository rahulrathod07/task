 #!/bin/sh

# sudo docker run --network="host" --name dummy-mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=fyndimdb -d mysql:5.7.33
# sudo docker run -p 3306:3306 --name dummy-mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:5.7.33
# sudo docker run --name=mysql-server -d mysql/mysql-server:latest

export INITIALIZE_DB=false
export DB_USERNAME="b8d20ec0f53090"
export DB_PASSWORD="46cce531"
export DB_SERVER_NAME="us-cdbr-east-03.cleardb.com"
export DB_NAME="heroku_a9c1dd5c5ec85b3"
export SECRET_KEY=thisissupersecretkey

python run.py
#mysql://b8d20ec0f53090:46cce531@us-cdbr-east-03.cleardb.com/heroku_a9c1dd5c5ec85b3?reconnect=true