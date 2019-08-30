# Using lightweight alpine image
FROM python:3.6-alpine

# Installing packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Defining working directory and adding source code
WORKDIR /usr/src/app
COPY bootstrap.sh requirements.txt ./
COPY cashman ./cashman

# Install packages
RUN pip install -r requirements.txt

# Start app
EXPOSE 5000
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]