FROM python:3.9.17-alpine
RUN pip install boto3
RUN pip install flask
RUN pip install prometheus_client
COPY aplicacao.py /aplicacao.py
CMD ["python3","aplicacao.py"]