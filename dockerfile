FROM python:3.14
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["python3", "-u", "/app/genconhotelsv3.py"]