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

    <!-- Custom CSS -->
    <link rel="stylesheet" href="static/css/frontEnd.css">

    <!-- jQuery library -->
    <script src="static/js/jquery.min.js"></script>
    <!-- Latest compiled JavaScript -->
    <script src="static/js/bootstrap.min.js"></script>

    <!-- Custom JS -->
    <script src="static/js/pageHandler.js"></script>
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
                <a href="{{link}}" class="btn azm-social azm-btn azm-google-plus col-xs-5 col-xs-push-7"><i class="fa fa-google-plus"></i>{{signin_state}}</a>
                % end
            </div>
        </div>
        <div id="result-title" class="text-left">
            <a href="/"><img src="static/img/title_small.png"></a>
        </div>
        <div>
            <form id="results-form" action="" method="get">
                <div class="row">
                    <div class="col-md-10 col-xs-8">
                        <div class="form-group form-group-lg">
                        <div class="input-group">
                            <div id="search_opt_list" class="input-group-btn">
                                <button id="toggle_image_search" type="button" class="btn btn-lg search_opt">Image</button>
                                <button id="toggle_video_search" type="button" class="btn btn-lg search_opt">Video</button>
                            </div>
                            <input id="search_input" spellcheck="true" type="text" name="keywords" class="form-control" value="{{queryInput}}">
                        </div>
                    </div>
                    </div>
                    <div class="col-md-2 col-xs-4">
                        <input type="submit" class="btn btn-primary btn-lg btn-block" value="Search">
                    </div>
                </div>
            </form>
        </div>

        <h1> Search for "{{queryInput}}" </h1>
        % if not spellcheck:
            <h4 id="spell-check-h4" class="inline-block">
                Did you mean? <a href="{{correct_link}}"><strong><i>{{corrected_search}}</i></strong></a>
            </h4>
        % end
        <h2>Results</h2>
        % if math != None:
        <div id="math_out">
            <div class="panel panel-default">
                <div class="panel-body"><i class="fa fa-4x fa-calculator" aria-hidden="true"></i><h4>{{queryInput}}</h4><h1> = {{math}}</h1></div>
            </div>
        </div>
        % end
        <div id="resultContent">
            % if len(siteList) == 0:
                <div class="panel panel-default">
                  <div class="panel-body"><h4>No Results Found</h4></div>
                </div>
            % else:
                %for url, rank, title, desc in siteList:
                    <div class="panel panel-default">
                      <div class="panel-body">
                          <h4><a class="a_link" href="{{url}}">{{title}}</a></h4>
                          <p class="cite">{{url}}</p>
                          <p>{{desc}}</p>
                      </div>
                    </div>
                % end
                <nav aria-label="Page navigation">
                  <ul class="pagination pagination-lg">
                    <li class="page-item">
                      <a class="a_link page-link-prev" aria-label="Previous">
                        <span aria-hidden="true">&laquo;</span>
                        <span class="sr-only">Previous</span>
                      </a>
                    </li>
                    %for i in range(1, ((pg_tot - 1) / 5) + 2):
                        % if i == page:
                            <li class="page-item active"><a id="page-{{page}}" class="a_link page-link page-link-cur">{{i}}</a></li>
                        % else:
                            <li class="page-item"><a id="page-{{i}}" class="a_link page-link">{{i}}</a></li>
                        % end
                    % end
                    <li class="page-item">
                      <a class="a_link page-link-next" aria-label="Next">
                        <span aria-hidden="true">&raquo;</span>
                        <span class="sr-only">Next</span>
                      </a>
                    </li>
                  </ul>
                </nav>
            %end
        </div>

    </div>
</body>
</html>