FROM python:3.8

COPY flask_mock.py /mock/flask_mock.py
WORKDIR /mock

RUN python -m pip install flask

EXPOSE 5000
CMD ["python", "flask_mock.py"]