FROM python:3.10-bullseye

WORKDIR /app

#install the requirements
COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /temp/requirements.txt
RUN rm -f /temp/requirements.txt

COPY wait-for-it.sh wait-for-it.sh
RUN chmod 0755 wait-for-it.sh