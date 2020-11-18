FROM python:3
MAINTAINER Piotr Frohlich
COPY . /app
WORKDIR /app
ENV ctrl_ip="172.17.0.1"
ENV mongo_db="172.17.0.1"
ENV update_window=100
RUN pip install -r ./requirements.txt
CMD python3 ./main.py $ctrl_ip $mongo_db $update_window