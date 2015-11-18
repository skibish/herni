# Interface

> Interface for Herñi

## Run

To run application you only need to run server and point it to the public folder.

Because it is an app with static files only, preferred way is to serve it with [http-server](https://github.com/indexzero/http-server).

Install it globally and then:

```bash
$ cd interface

$ http-server
```

App will be available on `localhost:8080`

## Develop

If you would like to develop: it is an [React](https://github.com/facebook/react) + [Babel](https://github.com/babel/babel) application.

Run `npm install` to install dependencies.

Install dev tools globally: `npm install -g browserify babel`

To build main js file run `browserify -t babelify app/app.js -o public/js/app.js`
