var Scraper = require ('images-scraper')
  , google = new Scraper.Google();
 

google.list({
    keyword: process.argv[2],
    num: process.argv[3],
    detail: true,
    nightmare: {
        show: true
    }
})
.then(function (res) {
    console.log(res);
}).catch(function(err) {
    console.log('err', err);
});
 
// you can also watch on events 
google.on('result', function (item) {
    console.log('out', item);
});

