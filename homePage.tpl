<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Define the page header -->
    <link rel="shortcut icon" href="static/header.png" />
    <title>Random Search</title>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="static/bootstrap.min.css">
    <link rel="stylesheet" href="static/styles.css">
    <link rel="stylesheet" href="static/font-awesome.min.css">
    <link rel="stylesheet" href="static/animate.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="static/frontEnd.css">

    <!-- jQuery library -->
    <script src="static/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="static/bootstrap.min.js"></script>
    <script src="static/math.js"></script>
    <script src="static/doMath.js"></script>
    <script src="static/frontEnd.js"></script>
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
            <img id="logo" class="animated zoomIn" src="static/title.png">
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