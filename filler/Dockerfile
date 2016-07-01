FROM ruby:2.3.0

ENV PORT 4568
ENV LOGIC_PORT 4567

ADD . /app/

RUN cd /app && bundle install

# Create user and give permissions
RUN useradd -ms /bin/bash usafe
RUN chown -R usafe:usafe /app

WORKDIR /app

USER usafe

EXPOSE $PORT

CMD ["ruby", "app.rb"]
