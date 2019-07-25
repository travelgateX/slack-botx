FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app

# copy rexources
COPY ./resources /app/resources
COPY ./contrib   /app/contrib

# install additional dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt