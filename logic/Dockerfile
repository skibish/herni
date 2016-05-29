FROM python:2.7

ENV PORT 4567
ENV CHARGER_URL http://charger:6082
ENV FILLER_URL http://filler:4568

ADD . /app/

WORKDIR /app

RUN pip install flask requests

# Create user and give permissions
RUN useradd -ms /bin/bash usafe
RUN chown -R usafe:usafe /app

USER usafe

EXPOSE $PORT

CMD ["python", "logic.py"]
