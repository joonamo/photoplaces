var sidebar_display_monthly_data;

function init_sidebar() {
    // Init diagram
    var target_div = $("#sidebar_stats_diagram");

    // Help from http://bl.ocks.org/mbostock/7441121
    var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 400 - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var chart = d3.select(".sidebar_chart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var x_axis_visual = chart.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")");

    var y_axis_visual = chart.append("g")
        .attr("class", "y axis");

    sidebar_display_monthly_data = function(data) {
        y.domain([0, d3.max(data)]);

        for (i in data) { 
            data[i] = [parseInt(i) + 1, data[i]];
        }

        x.domain(data.map(function(d) { return d[0]; }));
        x_axis_visual.call(xAxis);
        y_axis_visual.call(yAxis);

        bars = chart.selectAll(".bar")
            .data(data);

        bars.enter()
            .append("rect")
            .attr("class", function(d) { return "bar month_" + d[0]; })
            .attr("x", function(d) { return x(d[0]); })
            .attr("width", x.rangeBand());

        bars.transition().duration(500)
            .attr("y", function(d) { return y(d[1]); })
            .attr("height", function(d) { return height - y(d[1]); });
    }

    sidebar_display_monthly_data([0,0,0,0,0,0,0,0,0,0,0,0]);

}

function sidebar_display_cluster_info(id) {
    $.ajax({
        type: "GET",
        url: "rest/cluster_get_stats",
        dataType: "json",
        data: {id: id}
    })
        .done(function(msg){
            chart_data = []
            for (var i = 0; i < 12; i++){
                chart_data.push(msg["points_month_" + (i + 1)]);
            }
            sidebar_display_monthly_data(chart_data);
        });
    
    $("#sidebar_photos").html("<p>Loading photos...</p>");
    $.ajax({
        type: "GET",
        url: "ajax/sidebar_photos",
        dataType: "html",
        data: {id: id}
    })
        .done(function(msg){
            $("#sidebar_photos").html(msg);
        });
}