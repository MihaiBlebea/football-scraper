FROM python:3

WORKDIR ./app

COPY ./*.py ./

RUN pip3 install flask

RUN pip3 install requests

CMD ["python3", "main.py"]