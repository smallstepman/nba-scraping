FROM python:3.8
RUN pip install pipenv
COPY Pipfile* /app/
WORKDIR /app 
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app/
# RUN pip install /app/myapp
CMD flask run --host=0.0.0.0 --port=5000