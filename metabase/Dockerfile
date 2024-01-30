FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt /app/
COPY sql_test_app.py /app/
#RUN pip install -r requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "sql_test_app.py"]
