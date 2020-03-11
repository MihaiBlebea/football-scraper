FROM python:3

WORKDIR ./app

COPY ./*.py ./

RUN pip3 install flask

RUN pip3 install pymysql

RUN pip3 install requests

RUN pip3 install redis

CMD ["python3", "main.py"]