console.log("FOO")
var socket = io.connect("http://127.0.0.1:3000")
socket.on("tweet", function(data) {
  console.log(data)
  d3.select("body")
    .append("div")
    .text(data.body)
});

