FROM python:3.9 

ADD src/server.py /

RUN pip install crypt os pwd socket spwd ssl subprocess threading time

CMD [“python”, “./src/server.py”] 

EXPOSE 8080
