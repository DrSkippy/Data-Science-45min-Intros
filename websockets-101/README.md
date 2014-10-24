#Websockets 101

The first goal is to setup a simple HTML webpage that serves out a form and a list of messages. We're going to use the Node.JS web framework express to this end. Make sure Node.JS is installed.

First let's create a package.json manifest file that describes our project. I recommend you place it in a dedicated empty directory (I'll call mine chat-example).

<pre>
{
  "name": "socket-chat-example",
  "version": "0.0.1",
  "description": "my first socket.io app",
  "dependencies": {}
}
</pre>

Now, in order to easily populate the dependencies with the things we need to use the following commands:  
<pre>
npm install --save express
npm install socket.io --save
npm install oboe  --save
npm install express-device  --save
</pre>

Now that express is installed we can create an index.js file that will setup our application.

<pre>
<code>
var app = require('express')();
var http = require('http').Server(app);

app.get('/', function(req, res){
  res.send('<h1>Hello world</h1>');
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
</code>
</pre>

This translates into the following:

*  Express initializes app to be a function handler that you can supply to an HTTP server (as seen in line 2).
*  We define a route handler / that gets called when we hit our website home.
*  We make the http server listen on port 3000.

If you run `node index.js` you should see the terminal `listening on
*:3000`. Point your browser to `http://localhost:3000` to see the html
that you are sending. 

Serving HTML
So far in `index.js` we're calling res.send and pass it a HTML string. Our code would look very confusing if we just placed our entire application's HTML there. Instead, we're going to create an `index.html` file and serve it.
