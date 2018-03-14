var cors = require('cors');
var express = require('express');
var request = require('request');
var app = express();
 
/*app.use(cors({
    allowedOrigins: [
        'local.att.com', 'localhost', '127.0.0.1', "local.att.com:3000"
    ]
}))*/

app.options('*', cors({origin: true, credentials: true}));

app.get('*', cors({origin: true, credentials: true}), function (req, res) {
  request(req.query.url).pipe(res);
})
 
app.listen(8080);
