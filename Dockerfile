FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app /app/app

# copy rexources
COPY ./contrib   /app/contrib

# prometheus multiproc (gunicorn)
ENV prometheus_multiproc_dir multiproc-tmp
RUN mkdir $prometheus_multiproc_dir

# install additional dependencies
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt