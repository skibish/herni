var express = require('express');
var request = require('request');

var apiServerHost = process.env.LOGIC_URL;
var chargerUrl = process.env.CHARGER_URL;
var fillerUrl = process.env.FILLER_URL

var app = express();

var options = {
  method: 'POST',
  url: apiServerHost + '/init',
  body: {filler_url: fillerUrl, charger_url: chargerUrl},
  json: true
};

// vending machine initialization
request(options);

app.use(express.static('public'));

app.get('/',function(req,res){
     res.sendFile('public/index.html');
});

app.use('/api', function(req, res) {
  var url = apiServerHost + req.url;
  req.pipe(request(url)).pipe(res);
});

app.listen(process.env.PORT || 3000);
