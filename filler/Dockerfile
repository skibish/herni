FROM ruby:2.3

ENV PORT 4568
ENV LOGIC_PORT 4567

ADD . /app/

WORKDIR /app

RUN bundle install

# Create user and give permissions
RUN useradd -ms /bin/bash usafe
RUN chown -R usafe:usafe /app

USER usafe

EXPOSE $PORT

CMD ["ruby", "app.rb"]
