FROM python:3.12-slim
WORKDIR .
ARG OPENAI_API_KEY=1
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
COPY Pipfile.lock ./
RUN pip install pipenv
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "src/app.py"]