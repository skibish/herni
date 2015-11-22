# Interface

> Interface for Herñi

## Run

Install everything with `npm install --production` command.

Start server with `node server.js` command.

App will be available on `localhost:3000`

MUST HAVE FOLLOWING ENV VARIABLES:
 - PORT (default 3000, but you can change to desired)
 - LOGIC_URL (endpoint of `logic` service)
 - CHARGER_URL (endpoint of `charger` sevice)
 - FILLER_URL (endpoint of `filler`)

## Develop

If you would like to develop: it is an [React](https://github.com/facebook/react) + [Redux](https://github.com/rackt/redux) + [Babel](https://github.com/babel/babel) application.

Run `npm install` to install all dependencies.

Install dev tools globally: `npm install -g browserify babel`

To build main js file run `browserify -t babelify app/app.js -o public/js/app.js`
