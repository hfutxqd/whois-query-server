FROM python:3.7

RUN apt-get update
RUN apt-get install -y redis-server

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["bash"]
CMD ["start.sh"]