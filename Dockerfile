FROM python:3.12-slim
WORKDIR .
COPY Pipfile.lock ./
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "src/app.py"]