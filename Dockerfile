FROM hub.hamdocker.ir/library/python:3.8
WORKDIR /lovinoo/
ADD ./requirements.txt ./
RUN pip install -r ./requirements.txt
ADD ./ ./
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 lovinoo.wsgi"]