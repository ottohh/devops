FROM ubuntu:22.04

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==3.0.* gunicorn

# install app
COPY storage.py /

# final configuration
CMD ["gunicorn", "--bind", "0.0.0.0:8198", "storage:app"]