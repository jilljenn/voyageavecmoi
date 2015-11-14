var express = require('express');
var path = require('path');
var httpProxy = require('http-proxy');

var proxy = httpProxy.createProxyServer();
var app = express();

var isProduction = process.env.NODE_ENV === 'production';
var port = isProduction ? 80 : 8085;
var publicPath = path.resolve(__dirname, 'src', 'public');

app.use(express.static(publicPath));

// We proxyfie all API requests under the /api route
app.all('/api/*', function(req, res) {
    proxy.web(req, res, {
        target: 'http://localhost:5000'
    });
});

// We only want to run the workflow when not in production
if (!isProduction) {

    // We require the bundler inside the if block because
    // it is only needed in a development environment. Later
    // you will see why this is a good idea
    var bundle = require('./server/bundle.js');
    bundle();

    // Any requests to localhost:8080/build is proxied
    // to webpack-dev-server
    app.all('/build/*', function(req, res) {
        proxy.web(req, res, {
            target: 'http://localhost:8090'
        });
    });

}

proxy.on('error', function(e) {
    console.log('Could not connect to proxy, please try again...');
});

app.listen(port, function() {
    console.log('Server running on port ' + port);
});
