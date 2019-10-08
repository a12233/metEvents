FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python main.py --bind 0.0.0.0:5000 wsgi
