FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD docker_reg.py reg_test/docker_reg.py
WORKDIR ./reg_test
CMD python3 docker_reg.py
