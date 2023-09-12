FROM python:3.11-alpine

ENV PROJ_DIR="/app"
ENV LOG_FILE="${PROJ_DIR}/app.log"
ENV CRON_SPEC="0 8 * * *"

WORKDIR ${PROJ_DIR}
COPY requirements.txt .
RUN touch ${LOG_FILE}

RUN pip install -r requirements.txt
RUN crontab -l | { cat; echo "${CRON_SPEC} /usr/local/bin/python3 ${PROJ_DIR}/main.py"; } | crontab -

COPY . .

CMD crond  && tail -f ${LOG_FILE}
