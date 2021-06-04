FROM python:3.6


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -yyq netcat


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY ./entrypoint.sh .


COPY . .


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]