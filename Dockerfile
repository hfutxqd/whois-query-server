FROM python:3.7

WORKDIR /app

COPY . .

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["server.py"]