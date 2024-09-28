FROM --platform=$BUILDPLATFORM python:3.11-slim-bookworm
EXPOSE 8000
RUN mkdir /var/log/my_website
WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app/
RUN python manage.py collectstatic
CMD ["gunicorn", "cdn_dashboard.wsgi:application", "-b", ":8000", "--access-logfile", "/var/log/my_website/gunicorn_access.log", "--error-logfile", "/var/log/my_website/gunicorn_error.log"]