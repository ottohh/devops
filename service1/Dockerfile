FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.* gunicorn
RUN pip install psutil requests

# install app
COPY service1.py /

# final configuration
EXPOSE 8199
CMD ["gunicorn", "--bind", "0.0.0.0:8199", "service1:app"]