FROM php:7

# Define global port variable
ENV PORT 6082

# Copy app to container
ADD . /app/

RUN apt-get update

# Download composer, install dependencies, remove it
RUN cd /app \
  && apt-get install -y zip unzip git \
  && curl https://getcomposer.org/installer --output composer-setup.php \
  && php composer-setup.php \
  && php composer.phar install \
  && rm composer-setup.php composer.phar \
  && apt-get remove -y zip unzip git \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create user and give permissions
RUN useradd -ms /bin/bash usafe
RUN chown -R usafe:usafe /app

# index.php is in public, so we will run there
WORKDIR /app/public

USER usafe

EXPOSE $PORT

CMD ["/bin/bash", "-c", "php -S 0.0.0.0:$PORT"]
