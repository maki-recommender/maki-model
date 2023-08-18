# maki recommender api
FROM python:3.9.16-slim-bullseye

EXPOSE 5000


# install dependency directly inside the container
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ease /ease
COPY ./exceptions.py .
COPY ./models.py .
COPY ./utils.py .
COPY ./main.py .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
