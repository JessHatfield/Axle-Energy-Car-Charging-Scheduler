FROM python:3.12
LABEL authors="jesshatfield"

COPY requirements.txt /app/
WORKDIR /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /app/

ENV ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=CarChargingScheduler.settings

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py generate_dummy_data
RUN python manage.py check --deploy

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CarChargingScheduler.wsgi:application"]