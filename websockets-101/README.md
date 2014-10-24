#Websockets 101

This intro is a combination of a tutorial on [socket.io](http://socket.io/get-started/chat/) and wisdom gleamed from [Erik Cunningham](https://twitter.com/trinary). 

The first goal is to setup a simple HTML webpage using the Node.JS web framework express. Make sure Node.JS is installed.

We'll start creating dependencies in `package.json`:
<pre>
{
  "name": "websocket-example",
  "version": "0.0.1",
  "description": "my first socket.io app",
  "dependencies": {}
}
</pre>

To populate the dependencies we run the following commands:  
<pre>
npm install --save express
npm install socket.io --save
npm install oboe  --save
npm install express-device  --save
</pre>

Now that express is installed we can create an `index.js` file that will setup our application.
```html
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function(req, res){
  res.send('<h1>Hello world</h1>');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
```

According to the folks at socket.io, the above lines of code translate into the following:

*  Express initializes app to be a function handler that you can supply to an HTTP server (as seen in line 2).
*  We define a route handler / that gets called when we hit our website home.
*  We make the http server listen on port 3000.

Run `node index.js` and you should see the terminal `listening on *:3000`. Point your browser to `http://localhost:3000` to see the html that you are sending. 

So far in `index.js` we're calling res.send and pass it an HTML string, but it's more common to send an html file. So let's refactor our route handler in `index.js` to use sendfile instead:  

<pre>
app.get('/', function(req, res){
  res.sendFile('index.html');
});
</pre>

And populate `index.html` with the following:  

```html
<head>  
  <script src = "/app.js"></script>
  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
</head>
<body>
  <H1> HELLO WORLD  </H1>
  <p> (from a file)  </p>
</body>
```  

Refresh your browser and you'll see the file being used.

# Integrating Socket.io
Socket.IO is composed of two parts:

1.  A server that integrates with (or mounts on) the Node.JS HTTP Server: socket.io
2.  A client library that loads on the browser side: socket.io-client

We'll add socket.io with an edit to `index.js`:

```html
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendfile('index.html');
});

io.on('connection', function(socket){
  console.log('a user connected');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
```
We just "initializ[ed] a new instance of socket.io by passing the http (the HTTP server) object. Then [we] listen on the connection event for incoming sockets, and log it to the console."

We need to load the socket.io-client in `index.html`:
```html
<head>
  <script src="/socket.io/socket.io.js"></script>
  <script src = "/app.js"></script>
  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
</head>
<body>
  <H1> HELLO WORLD  </H1>
  <p> (from a file)  </p>
</body>
<script>
  var socket = io();
</script>
```

If you now reload the server and the website you should see the console print "a user connected".
Try opening several tabs, and you'll see several messages.

# Emmiting Realtime Data

We're now going to use Powertrack to get a feel for the current state of
BELIEBER-ism.

First, you'll need to provide your gnip console creds:

<pre>
export POWERSOCKET_USER=
export POWERSOCKET_PATH=
export POWERSOCKET_PASS=
export PORT=3000
</pre>

Next, we need to learn about emmitting data. The result of the following
code is that we're going to send complete json records from the server
to the browser using io.sockets.emit(). 

<pre>
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
</pre>

In the `index.html` document, we pull in the socket.io client, make d3
available and define the path for app.js. 

```html
<head>  
  <script src = "/socket.io/socket.io.js"></script>
  <script src = "/app.js"></script>
  <script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
</head>
<body>
  <H1> NOTES FROM BELIEBERs </H1>
</body>
```

Our `app.js` script is what does the work with the data. When this
script is called, we can log information to the console or affect the
html with d3. 

<pre>
console.log("FOO")
var socket = io.connect("http://127.0.0.1:3000")
socket.on("tweet", function(data) {
  console.log(data)
  d3.select("body")
    .append("div")
    .text(data.body)
});
</pre>

We can now run `node index.js` and watch the magic of the beliebers
unfold.

