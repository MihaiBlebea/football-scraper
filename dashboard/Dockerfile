FROM python:3

WORKDIR ./app

COPY ./*.py ./

COPY ./templates/*.html ./templates/

RUN pip3 install flask

RUN pip3 install requests

RUN pip3 install redis

EXPOSE 8081

CMD ["python3", "main.py"]