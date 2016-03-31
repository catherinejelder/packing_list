FROM python:3.5.1
COPY . /usr/src/app/
EXPOSE 8080
CMD ["python", "-u", "/usr/src/app/server.py"]
