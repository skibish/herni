var express = require('express');
var request = require('request');

var apiServerHost = process.env.LOGIC_URL

var app = express();

app.use(express.static('public'));

app.get('/',function(req,res){
     res.sendFile('public/index.html');
});

app.use('/api', function(req, res) {
  var url = apiServerHost + req.url;
  req.pipe(request(url)).pipe(res);
});

app.listen(process.env.PORT || 3000);
