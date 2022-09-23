FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt


# production setting
COPY ./src/ /app/
ENV FLASK_APP /app/app.py
ENV FLASK_ENV production
CMD flask run -h 0.0.0.0 -p $PORT
