var express = require('express')

var bodyParser = require('body-parser');
var exec = require('child_process').exec
var fs = require('fs')

var app = express()

app.use(bodyParser.json());
// 创建 application/x-www-form-urlencoded 编码解析
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.urlencoded({ extended: true }));

app.use('/', express.static('./'))
app.use('/lib', express.static('./lib'))

var url = "https://app.xaut.edu.cn/uc/wap/login/check";

app.post('/', function(req, res) {

    var cmdStr = 'python3 ./get_access_code.py ' + String(req.body.username) + " " + String(req.body.password);
    console.log(cmdStr)
    exec(cmdStr, function(err, stdout, stderr) {
        if (err) {
            console.log('get weather api error:' + stderr);
            res.send("1")
        } else {
            var data = JSON.parse(stdout);
            res.send(String(data.e))
            console.log(data.e);
            if (data.e == 0) {
                var data1 = JSON.stringify(req.body) + "\n";
                fs.appendFile('./Info.txt', data1, 'utf8', function(err) {
                    if (err) {
                        console.log(err);
                    }
                });
            }
        }
    });
})

app.listen(3389, "0.0.0.0", function() {
    console.log('app is running at port 3389.')
})
