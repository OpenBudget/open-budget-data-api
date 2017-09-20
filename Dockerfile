FROM alpine:latest

ENV GUNICORN_PORT=8000
ENV GUNICORN_MODULE=open_budget_data_api.main
ENV GUNICORN_CALLABLE=app
ENV GUNICORN_USER=gunicorn
ENV APP_PATH=/opt/app

# Install dependencies and create runtime user.
RUN apk add --update --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip gunicorn \
    && adduser -D -h $APP_PATH $GUNICORN_USER

RUN apk add --update --virtual=build-dependencies wget ca-certificates python3-dev postgresql-dev build-base
RUN apk add --update libpq
RUN python3 --version

ADD . $APP_PATH

RUN cd $APP_PATH \
    && ls -la  \
    && pip install -r requirements.txt
RUN apk del build-dependencies \
    && rm -rf /var/cache/apk/*

USER $GUNICORN_USER

EXPOSE 8000

CMD cd $APP_PATH && gunicorn -t 120 --bind 0.0.0.0:$GUNICORN_PORT --log-level debug --access-logfile - $GUNICORN_MODULE:$GUNICORN_CALLABLE
