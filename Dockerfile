# maki recommender api
FROM python:3.10-slim-bullseye 

EXPOSE 50051


# install dependency directly inside the container
COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools \
    pip install --no-cache-dir -r requirements.txt

COPY ./models /models
COPY ./proto /proto
COPY ./recommendations.py .
COPY ./utils.py .
COPY ./trainer.py .
COPY ./main.py .


CMD python main.py
