FROM python:3.7-slim

RUN apt update 
RUN apt -y upgrade 

ADD requirements-docker.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# create user 
ARG user=genesis
ARG group=genesis
ARG uid=1000
ARG gid=1001
RUN adduser ${user}

USER ${user}
RUN mkdir /home/${user}/src
RUN mkdir /home/${user}/log

# cp project files 
ADD app/ /home/${user}/src/app/
ADD model_dir/ /home/${user}/src/model_dir
ADD index_to_name.json /home/${user}/src/
ADD genesis-gunicorn.sh /home/${user}/src/

# EXPOSE 8000

CMD ["sh", "/home/genesis/src/genesis-gunicorn.sh"]