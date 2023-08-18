# maki recommender api
FROM python:3.9.16-slim-bullseye

EXPOSE 50051


# install dependency directly inside the container
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./models /models
COPY ./proto /proto
COPY ./recommendations.py .
COPY ./utils.py .
COPY ./main.py .


CMD ["python" "main.py"]
