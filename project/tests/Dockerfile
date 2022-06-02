FROM python:3.8

ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt && rm -f /requirements.txt

CMD ["/tests/start_tests.sh"]