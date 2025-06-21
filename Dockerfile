FROM python:3.10

WORKDIR /camlin
COPY . /camlin

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["bash", "launch.sh"]
