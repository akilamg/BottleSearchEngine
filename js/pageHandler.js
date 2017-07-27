$(document).ready(function(){
    $("div.container").on("click", "a.page-link", function(){
        var page = $(this).html();
        var pathname = window.location.href;
        if( !$(this).hasClass("page-link-cur") )
            sendPageUpdate(page, pathname);
    });

    $("div.container").on("click", "a.page-link-prev", function(){
        var page = parseInt( $("a.page-link-cur").attr("id").split("-")[1] ) - 1;
        var pathname = window.location.href;

        if (page > 0)
            sendPageUpdate(page, pathname);
    });

    $("div.container").on("click", "a.page-link-next", function(){
        var page = parseInt( $("a.page-link-cur").attr("id").split("-")[1] ) + 1;
        var pathname = window.location.href;

        if (page <= $("a.page-link").length)
            sendPageUpdate(page, pathname);
    });

    function sendPageUpdate(page, pathname){
        $.ajax({
            url: pathname + "&page=" + page,
            type:"GET",
            success: function(result){
                $("#resultContent").html(result);
            },
        })
    }
});