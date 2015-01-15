var map;
var bounds = new google.maps.LatLngBounds ();
var markers = {};
var cluster_polygons = {};
var zoomTimeout;
var marker_image = {
    url: "/static/images/red_marker.png",
    anchor: new google.maps.Point(4,4)}

function createMap() {
    var mapOptions = {
      center: new google.maps.LatLng(0, 0),
      zoom: 1,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("canvas"),
        mapOptions); 

    // google.maps.event.addListener(map, 'bounds_changed', function(e) {
    //     if (zoomTimeout) {
    //         window.clearTimeout(zoomTimeout);
    //     }
    //     zoomTimeout = window.setTimeout(query_points_for_view, 5000);
    // })

}

function query_points_for_view() {
    var bounds = map.getBounds();
    var x0 = bounds.getNorthEast().lng();
    var y0 = bounds.getNorthEast().lat();
    var x1 = bounds.getSouthWest().lng();
    var y1 = bounds.getSouthWest().lat();

    // Remove stuff off screen
    var to_remove = [];

    // What to remove
    $.each(markers, function(idx, marker){
        if (!bounds.contains(marker.getPosition()))
        {
            marker.setMap(null);
            to_remove.push(idx);
        }
    });
    $.each(to_remove, function(i, idx){
        delete markers[idx];
    })

    // $.getJSON("/rest/photos_box_contains?x0=" + x0 + "&y0=" + y0 + "&x1=" + x1 + "&y1=" + y1, function(data){
    //     console.log("got " + data.features.length);
    //     add_photo_to_map(data.features, 0, 128);
    // })

    $.getJSON("/rest/clusters_box_contains?x0=" + x0 + "&y0=" + y0 + "&x1=" + x1 + "&y1=" + y1, function(data){
        console.log("got " + data.features.length);
        add_cluster_to_map(data.features, 0);
    })

}

function create_photo_marker(photo_info) {
    var loc = new google.maps.LatLng(photo_info.geometry.coordinates[1], photo_info.geometry.coordinates[0]);
    var marker = new google.maps.Marker({
        map: map,
        position: loc,
        icon: marker_image
    });

    var infowindow = new google.maps.InfoWindow({
        content: "<div style='width:200px;height:200px'><a href='" + photo_info.properties.photo_url + "'><img src='" + photo_info.properties.photo_thumb_url + "' style='max-width:100%;max-height:100%;'/></div>"
        }); 
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.open(map,marker);
        });
    markers[photo_info.id] = marker;
}

function add_photo_to_map(photos, i, step) {
    for (var j = 0; j < step; j++) {
        if (i + j >= photos.length)
        {
            break;
        }
        var photo_info = photos[i + j];
        if (!markers[photo_info.id]) {
            create_photo_marker(photo_info);
        }
    }
    i += step;
    if (i < photos.length) {
        window.setTimeout(function(){add_photo_to_map(photos, i, step);}, 1);
    }
}

function add_cluster_to_map(clusters, i){
    // Define the LatLng coordinates for the polygon's path.
    var cluster = clusters[i];
    var coords = [];
    for (j in cluster.geometry.coordinates[0])
    {   
        var c = cluster.geometry.coordinates[0][j];
        coords.push(new google.maps.LatLng(c[1], c[0]));
    }

    // Construct the polygon.
    var poly = new google.maps.Polygon({
    paths: coords,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35
    });

    poly.setMap(map);
    cluster_polygons[cluster.id] = poly;

    if (i < clusters.length - 1)
    {
        window.setTimeout(function(){add_cluster_to_map(clusters, i + 1);}, 1);
    }

}