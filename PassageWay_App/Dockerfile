FROM python:3.7.2-stretch

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

# Listen to port 5000 at runtime
EXPOSE 5000

# Define our command to be run when launching the container
CMD ["python", "app.py"]
