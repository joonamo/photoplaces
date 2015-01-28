var sidebar;

function init_sidebar() {
    sidebar = $("#sidebar");
}

function sidebar_display_cluster_info(id) {
    $.ajax({
        type: "GET",
        url: "rest/cluster_get_stats",
        //dataType: "json",
        data: {id: id}
    })
        .done(function(msg){
            sidebar.html(msg);
        });
}