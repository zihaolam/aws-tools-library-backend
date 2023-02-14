FROM lambci/lambda:build-python3.8

COPY . /app

RUN mv /app/lib/* /var/task
# manually add custom packages to python packages