FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN apt-get update && apt-get install python3-pip -y && pip3 install pandas==1.2.2 && pip3 install numpy==1.19.5 && pip3 install fastapi==0.68.0 && pip3 install uvicorn==0.14.0
COPY ./app /app

