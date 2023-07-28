FROM python:2.7.18
WORKDIR /mail_service
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
