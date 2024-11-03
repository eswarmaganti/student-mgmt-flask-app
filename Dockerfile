FROM python:3.12.7-slim-bullseye

# setting the application working diretory
WORKDIR /opt/SP/app

# copy the requirements.txt file and install dependencies
COPY requirements.txt ./

# install the requirements
RUN pip install -r requirements.txt

# copy the source code
COPY . .

# serving the application usng gunicorn server
ENTRYPOINT ["gunicorn"]
CMD ["-w", "4", "-t", "3", "--bind", "0.0.0.0:8000", "main:app"]