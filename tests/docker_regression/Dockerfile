FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD test_regression_endpoint.py /reg_test/test_regression_endpoint.py
WORKDIR reg_test
CMD python3 test_regression_endpoint.py
