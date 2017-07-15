$(document).ready(function(){

     $("#search_opt_list").on("click", ".search_opt", function(){
        var id = $(this).attr("id");
        var content = $(this).text();

        if(!$(this).hasClass("btn-primary")){
            var check = "<i class='fa fa-check'></i>";
            var name = id.split("_")[1] + "_keywords";
            var other_opts = $("#search_opt_list").find(".search_opt").not(this);

            $(other_opts).each(function(){
                var opt_content = $(this).text();
                $(this).removeClass("btn-primary");
                $(this).html(opt_content);
            });

            $("#search_input").attr("name", name);
            $(this).addClass("btn-primary");
            $(this).html(check + " " + content);

        }
        else{
            $("#search_input").attr("name", "keywords");
            $(this).removeClass("btn-primary");
            $(this).html(content);
        }

        $("#results-form input[type='submit']").trigger("click");
     });

     $("#resultContent").on("click", "img.click-img", function(){
        location.href = $(this).attr("src");
     });

    $("#resultContent").on("click", "img.click-thumb", function(){
        var src = $("#spell-check-h4").find(".a_link").attr("href");
        location.href = src;
     });
});