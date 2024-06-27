FROM python:3.11-slim

COPY ./requirements.txt .
COPY ./t_influencer_posts_202401121334.csv .
COPY ./tests /tests

RUN pip install -r requirements.txt

# WORKDIR /app

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
