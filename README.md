python3.9 -m venv ./venv2
source ./venv2/bin/activate

python3.9 -m pip install --upgrade pip
docker pull rabbitmq:3-management
docker run --rm -it -p 15672:15672 -p 5672:5672 rabbitmq:3-management


