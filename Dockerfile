FROM python:3.6-slim
WORKDIR /app
COPY requirements.txt /app/
COPY data_fetch.py /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "data_fetch.py"]
