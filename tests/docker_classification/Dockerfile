FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests
ADD test_classification_endpoint.py classif_test/test_classification_endpoint.py
WORKDIR /classif_test
CMD python3 test_classification_endpoint.py
