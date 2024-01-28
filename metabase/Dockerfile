FROM python:3
WORKDIR /app
COPY requirements.txt /app/
COPY sql_test_app.py /app/
RUN pip install -r requirements.txt
CMD ["python", "sql_test_app.py"]
