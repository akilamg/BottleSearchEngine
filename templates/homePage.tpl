<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Define the page header -->
    <link rel="shortcut icon" href="static/img/header.png" />
    <title>Random Search</title>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="static/css/bootstrap.min.css">
    <link rel="stylesheet" href="static/css/styles.css">
    <link rel="stylesheet" href="static/css/font-awesome.min.css">
    <link rel="stylesheet" href="static/css/animate.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="static/css/frontEnd.css">

    <!-- jQuery library -->
    <script src="static/js/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="static/js/bootstrap.min.js"></script>
    <script src="static/js/math.js"></script>
    <script src="static/js/doMath.js"></script>
    <script src="static/js/frontEnd.js"></script>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                % if user != None:
                <a href="#" class="btn dropdown-toggle azm-social azm-btn azm-google-plus col-xs-5 col-xs-push-7" data-toggle="dropdown">
                    <i class="fa fa-google-plus"></i> Signed in as {{user}} <b class="caret"></b>
                </a>
                <ul class="dropdown-menu dropdown-menu-right">
                    <li><a href="{{link}}" class="btn btn-lg">{{signin_state}}</a></li>
                </ul>
                % else:
                <a href="{{link}}" class="btn azm-social azm-btn azm-google-plus col-xs-3 col-xs-push-9"><i class="fa fa-google-plus"></i>{{signin_state}}</a>
                % end
            </div>
        </div>
        <!-- Define the page title -->
        <div id="pg-title" class="text-center">
            <img id="logo" class="animated zoomIn" src="static/img/title.png">
        </div>
        <form action="/" method="get">
            <div class="row">
                <div class="col-md-10 col-xs-8">
                    <div class="form-group form-group-lg">
                        <div class="input-group">
                            <div id="search_opt_list" class="input-group-btn">
                                <button id="toggle_image_search" type="button" class="btn btn-lg search_opt">Image</button>
                                <button id="toggle_video_search" type="button" class="btn btn-lg search_opt">Video</button>
                            </div>
                            <input id="search_input" spellcheck="true" type="text" name="keywords" class="form-control">
                        </div>
                    </div>
                </div>
                <div class="col-md-2 col-xs-4">
                    <input type="submit" class="btn btn-primary btn-lg btn-block" value="Search">
                </div>
            </div>
        </form>
    </div>
</body>
</html>