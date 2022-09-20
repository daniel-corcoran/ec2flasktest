FROM python:3.8-alpine
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY templates/ /deploy/templates/
COPY uploads/ /deploy/uploads/

WORKDIR /deploy/

RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]