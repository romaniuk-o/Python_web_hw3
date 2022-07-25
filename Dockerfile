FROM python:3.10

WORKDIR /hw3_romaniuk

COPY . /hw3_romaniuk

RUN pip install -r requirements.txt

CMD ["python", "main.py"]