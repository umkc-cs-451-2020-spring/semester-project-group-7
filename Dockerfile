FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
RUN chmod a+x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "commercebank.wsgi:application"]