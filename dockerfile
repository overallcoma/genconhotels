FROM python:3
RUN mkdir -p /app/
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-u", "/app/gencon-hotels-web2.py"]