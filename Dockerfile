FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app

# copy rexources
COPY ./contrib   /app/contrib

# install additional dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt