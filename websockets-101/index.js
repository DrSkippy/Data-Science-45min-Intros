//
'use strict';

// express magic (like py import)
var express = require('express');
var app = express();
var http = require('http');
var https = require('https'); // pt req
var server = http.createServer(app);
var io = require('socket.io').listen(server);
var device  = require('express-device');
var zlib = require('zlib'); // pt req (compressed streams are delievered from pt)
var fs = require('fs');
var oboe = require('oboe'); // streaming json parsing (sends complete records)

// pulls env variables
var username = process.env.POWERSOCKET_USER; 
var password = process.env.POWERSOCKET_PASS;
var path     = process.env.POWERSOCKET_PATH;
var runningPortNumber = process.env.PORT;

// pt setup options (headers: allowing any format (defult is json) and gzip the stream)
var requestOptions = {
    hostname: 'stream.gnip.com',
    port: 443,
    method: 'GET',
    path: path,
    auth: [username, password].join(':'),
    headers: { 'accept': '*/*',
               'accept-encoding': 'gzip' },
    rejectUnauthorized: false
};

// saves the options
requestOptions.agent = new https.Agent(requestOptions);



// logs every request
app.use(function (req, res, next) {
	// output every request in the array
	console.log({method: req.method, url: req.url, device: req.device});

	// goes onto the next function in line
	next();
});

// how the client get's the javascript to run
app.get('/', function (req, res) {
	res.sendfile('index.html', {});
});

// let's us serve the javascript
app.get('/app.js', function (req, res) {
	res.sendfile('app.js', {});
});

// res is the response from the server
var req = https.request(requestOptions, function (res) {
  console.log('Got a response, status: ', res.statusCode);
  // node stream system: pipe the output of res as input to zlib.createGunzip and then pass the output to oboe for json parsing
  oboe(res.pipe(zlib.createGunzip()))
    .done(function (d) {
          // callback for a complete object
          console.log('emitting');  
          // send the tweet event to everything that is listening.
          io.sockets.emit('tweet', d);
    });
});
req.end();

server.listen(runningPortNumber);
