FROM python:3.11-alpine

COPY requirements.txt .

RUN python3 pip install -r requirements.txt --no-cache-dir

RUN crontab -l | { cat; echo "0 8 * * * /usr/bin/python3 /root/asicscaner/main.py"; } | crontab -

WORKDIR /asicscaner

COPY . .

CMD cron && tail -f /var/log/cron.log
