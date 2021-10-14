FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD docker_classif.py classif_test/docker_classif.py
WORKDIR ./classif_test
CMD python3 docker_classif.py
