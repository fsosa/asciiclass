var restify = require('restify');
var mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/lab8');

var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function callback() {
	console.log("yay!");
});
var pickupSchema = mongoose.Schema({
	time: Date, 
	lat: Number, 
	'long': Number, 
});

var Pickup = mongoose.model('Pickup', pickupSchema);

var server = restify.createServer();

server.use(restify.queryParser());
server.use(restify.jsonp());

server.get('pickups?start=:start&end=:end)', function(req, res, next) {
	start = new Date(req.params.start).toISOString();
	end = new Date(req.params.end).toISOString();
	Pickup.where('time').gte(req.params.start).lte(req.params.end).select('lat long').limit(2500).exec(function(error, results) {
		if (error) {
			console.log("there was an error in the db!");
			res.send(error);
			return; 
		}	

		res.send(results);
	});
});

server.listen(8080, function() {
  console.log('%s listening at %s', server.name, server.url);
});
