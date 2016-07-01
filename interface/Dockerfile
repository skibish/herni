FROM node

ENV PORT 8080
ENV LOGIC_URL http://logic:4567

ADD . /app/

RUN cd /app \
  && npm install -g browserify babel \
  && npm install \
  && browserify -t babelify app/app.js -o public/js/app.js \
  && npm prune --production

# Create user and give permissions
RUN useradd -ms /bin/bash usafe
RUN chown -R usafe:usafe /app

WORKDIR /app

USER usafe

EXPOSE $PORT

CMD ["node", "server.js"]
