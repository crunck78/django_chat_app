# syntax=dockerfile:1
FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN /usr/local/bin//python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requitements.txt

COPY . .
RUN cd ./django_chat_app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]