FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD ./test_endpoint.py /test/test_endpoint.py
WORKDIR ./test
CMD python3 test_endpoint.py
