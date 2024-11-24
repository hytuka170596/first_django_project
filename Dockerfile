FROM python:3.10.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY mysite .

CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000"]
