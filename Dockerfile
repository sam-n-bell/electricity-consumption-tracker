FROM python:3.10-slim as install_py


WORKDIR /usr/src/app

FROM install_py as install_deps
RUN pip install pipenv==2023.3.20
COPY Pipfile /usr/src/app
COPY Pipfile.lock /usr/src/app
RUN pipenv install --system --deploy

FROM install_deps as start_app
COPY . /usr/src/app
ENV PYTHONPATH = /usr/src/app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

