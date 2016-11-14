FROM codexfons/gunicorn

USER root

RUN apk add --update --virtual=build-dependencies wget ca-certificates python3-dev postgresql-dev build-base
RUN apk add --update libpq
RUN python3 --version

ADD [a-z_A-Z]* $APP_PATH/
ADD open_budget_data_api $APP_PATH/open_budget_data_api
RUN ls -la /opt/app/
RUN pip install $APP_PATH
RUN apk del build-dependencies
RUN rm -rf /var/cache/apk/*

USER $GUNICORN_USER

ENV GUNICORN_MODULE=open_budget_data_api.main

EXPOSE 8000