FROM python:3.7-slim

ENV GUNICORN_PORT=8000
ENV GUNICORN_MODULE=open_budget_data_api.main
ENV GUNICORN_CALLABLE=app
ENV GUNICORN_USER=gunicorn
ENV APP_PATH=/opt/app

# RUN apk add --update --virtual=build-dependencies wget ca-certificates python3-dev postgresql-dev build-base libffi-dev
# RUN apk add --update libpq
RUN apt-get update && apt-get install --no-install-recommends -y libpq-dev && update-ca-certificates

# Install dependencies and create runtime user.
RUN pip3 install --upgrade pip gunicorn[gevent] \
    && adduser --disabled-password --home $APP_PATH $GUNICORN_USER

ADD . $APP_PATH

RUN cd $APP_PATH \
    && pip3 install -r requirements.txt

USER $GUNICORN_USER

EXPOSE 8000

CMD cd $APP_PATH && gunicorn -t 120 --bind 0.0.0.0:$GUNICORN_PORT -k gevent -w 8 --log-level debug --access-logfile - $GUNICORN_MODULE:$GUNICORN_CALLABLE
