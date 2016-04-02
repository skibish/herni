# Herñi
Herñi – a vending machine
> build with :heart: using microservices architecture and [Docker](https://www.docker.com/)

## Story

This project was built for one of the university courses. The idea to use [microservices architecture](http://martinfowler.com/articles/microservices.html) came from a problem, that everyone in the team wanted to write code in language of their choice.

That's why Docker came into the play. It perfectly applies for this kind of architecture.

## Architecture

![Herni architecture](/herni_architecture_diagram.png)

Application consists of four services:
 - Interface - frontend in another words. It render view and proxy requests to logic.
 - Logic - is a heart of application. All business logic is here.
 - Charger - emulates card charging.
 - Filler - fills vending machine with products.

## How to start

In terminal type:

```bash
$ docker-compose up -d
```

First time this command will build all images. Then it will reuse them to build containers.

Application will start on port `8080` of host machine or `docker-machine` (if [Docker Toolbox](https://www.docker.com/products/docker-toolbox) is used).

## Contribute

Feel free to contribute, improve services or add new.
