var map;
var bounds;
var markers = {};
var cluster_polygons = {};
var zoomTimeout;
var cluster_center_overlay;
var active_cluster_poly;
var marker_image;
var cluster_center_marker_icon;

function createMap() {
    bounds = new google.maps.LatLngBounds ();
    markers;
    cluster_polygons;
    marker_image = {
        url: STATIC_URL + "images/red_marker.png",
        anchor: new google.maps.Point(4,4)};
    cluster_center_marker_icon = {
        url: STATIC_URL + "images/transparent_marker_20_20.gif",
        size: new google.maps.Size(20, 20),
        anchor: new google.maps.Point(10,10)};

    var mapOptions = {
      center: new google.maps.LatLng(0, 0),
      zoom: 2,
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

function add_clustering_run_to_map(data){
    $.each(cluster_polygons, function(idx, poly){
        poly.setMap(null);
    });
    bounds = new google.maps.LatLngBounds ();
    cluster_polygons = [];
    cluster_center_overlay = new google.maps.OverlayView();

    cluster_center_overlay.onAdd = function() {
        var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
            .attr("class", "cluster_center");

        var projection = this.getProjection(),
                max_size = 100;
            var max_size_per_2 = max_size / 2;

        var marker = layer.selectAll("svg")
                .data(data.features)
                .each(transform)
            .enter().append("svg:svg")
                .each(transform)
                .each(tie_to_g_marker)
                .attr("class", "marker")
            .append("svg:g");

        marker.append("svg:polygon")
            .attr("points", function(cluster){
                var out = [];
                var last_phase = 0.0;
                var last_length = 1.0 / 12.0 * (max_size_per_2 - 1);
                var min_l = 0.0;//0.3 * max_size_per_2 * (Math.sqrt(cluster.properties.point_count_relative) * 0.7 + 0.3);
                for (var j = 1.0; j <= 12.0; j += 1.0){
                    var phase = j / 12.0 * 2 * Math.PI;
                    out.push([max_size_per_2 + Math.sin(last_phase) * min_l, max_size_per_2 - Math.cos(last_phase) * min_l]);
                    out.push([max_size_per_2 + Math.sin(phase) * min_l, max_size_per_2 - Math.cos(phase) * min_l]);

                    var second_poly = [];
                    var l = (Math.sqrt(cluster.properties["points_month_" + parseInt(j) + "_relative"]) * 0.7 + 0.3) * 
                        max_size_per_2 * (Math.sqrt(cluster.properties.point_count_relative) * 0.7 + 0.3);
                    second_poly.push([max_size_per_2 + Math.sin(last_phase) * min_l, max_size_per_2 - Math.cos(last_phase) * min_l]);
                    second_poly.push([max_size_per_2 + Math.sin(last_phase) * l, max_size_per_2 - Math.cos(last_phase) * l]);
                    second_poly.push([max_size_per_2 + Math.sin(phase) * l, max_size_per_2 - Math.cos(phase) * l]);
                    second_poly.push([max_size_per_2 + Math.sin(phase) * min_l, max_size_per_2 - Math.cos(phase) * min_l]);
                    second_poly.push(second_poly[0]);
                    last_phase = phase;
                    d3.select(this.parentElement)
                        .append("svg:polygon")
                        .attr("points", second_poly.join(" "))
                        .attr("class", "month_" + parseInt(j));
                }
                return out.join(" ");
            })
            .attr("class", "cluster_center_marker");

        function transform(cluster) {
            var coords = cluster.geometry.geometries[0].coordinates;
            var d = new google.maps.LatLng(coords[1], coords[0]);
            d = projection.fromLatLngToDivPixel(d);
            return d3.select(this)
                .style("left", (d.x - max_size_per_2) + "px")
                .style("top", (d.y - max_size_per_2) + "px");
        }

        function tie_to_g_marker(cluster){
            var coords = cluster.geometry.geometries[0].coordinates;
            var d = new google.maps.LatLng(coords[1], coords[0]);
            var marker = new google.maps.Marker({
                map: map,
                position: d,
                icon: cluster_center_marker_icon});
            var cluster_center = this;

            google.maps.event.addListener(marker, 'mouseover', function() {
                d3_cluster_center = d3.select(cluster_center)
                d3_cluster_center
                    .style("transform", "scale(3.0)")
                    .style("animation-name", "cluster_center_highlight")
                    .style("z-index", 1);
            });

            google.maps.event.addListener(marker, 'click', function() {
                if (active_cluster_poly) {
                    active_cluster_poly.setMap(null);
                }

                sidebar_display_cluster_info(d3_cluster_center[0][0].__data__.id);

                d3_cluster_center = d3.select(cluster_center)
                poly_bounds = new google.maps.LatLngBounds ();

                // Define the LatLng coordinates for the polygon's path.
                var coords = d3_cluster_center[0][0].__data__.geometry.geometries[1].coordinates[0];
                var g_coords = [];
                for (j in coords)
                {   
                    var c = coords[j];
                    var co = new google.maps.LatLng(c[1], c[0]);
                    g_coords.push(co);
                    poly_bounds.extend(co);
                }

                // Construct the polygon.
                var poly = new google.maps.Polygon({
                paths: g_coords,
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35
                });

                poly.setMap(map);
                active_cluster_poly = poly;

                map.fitBounds(poly_bounds);
            });

            google.maps.event.addListener(marker, 'mouseout', function() {
                d3.select(cluster_center)
                    .style("transform", "scale(1.0)")
                    .style("animation-name", "cluster_center_unhighlight")
                    .style("z-index", -1);
            });

            bounds.extend(d);
        }
        map.fitBounds(bounds);

        cluster_center_overlay.draw = function() {
            var projection = this.getProjection();
            layer.selectAll("svg")
                .data(data.features)
                .each(transform);            
        };
    };
    cluster_center_overlay.setMap(map);
}

function finalize_clustering_run_to_map(clusters){
    map.fitBounds(bounds);
}

function add_cluster_to_map(clusters, i){
    // Define the LatLng coordinates for the polygon's path.
    var cluster = clusters[i];
    var coords = [];
    var center = cluster.geometry.coordinates;
    bounds.extend(new google.maps.LatLng(
            center[1],
            center[0]));
    for (var j = 0.0; j < 12.0; j += 1.0)
    {   
        var phase = j / 12.0 * 2 * Math.PI;
        coords.push(new google.maps.LatLng(
            center[1] + Math.sin(phase) * 0.003, 
            center[0] + Math.cos(phase) * 0.003));
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
    cluster_polygons.push(poly);

    if (i < clusters.length - 1) {
        window.setTimeout(function(){add_cluster_to_map(clusters, i + 1);}, 1);
    } else {
        finalize_clustering_run_to_map(clusters);
    }

}

function show_all() {
    map.fitBounds(bounds);
}