var map = L.map('map'),
    realtime = L.realtime({
        url: 'http://wanderdrone.appspot.com/',
        //url: $SCRIPT_ROOT + 'random_gen',
        crossOrigin: true,
        type: 'json'
    }, {
        interval: 3 * 1000
    }).addTo(map);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

realtime.on('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 3});
    console.log("debug", $SCRIPT_ROOT);
});


