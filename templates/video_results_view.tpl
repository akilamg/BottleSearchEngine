% if len(vidList) == 0:
    <div class="panel panel-default">
      <div class="panel-body"><h4>No Results Found</h4></div>
    </div>
% else:
    %for title, url_comp, thumb_src in vidList:
        <div class="panel panel-default">
          <div class="panel-body">
              <img src="{{thumb_src}}" class="click-thumb">
              <h4><a class="a_link" href="https://www.youtube.com/watch?v={{url_comp}}">{{title}}</a></h4>
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