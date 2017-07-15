function isAlphaNumeric(str) {
    return /^[0-9a-zA-Z]+$/.test(str);
}
$(document).ready(function(){
    $('form').on('submit', function(){
        var input = $('input[type="text"]').val();
        if(input != '' && !isAlphaNumeric(input)){
            try {
                result = math.eval(input);
                 $('<input />').attr('type', 'hidden')
                .attr('name', 'math')
                .attr('value', result)
                .appendTo($(this));
            } catch(err) {
                console.log("ERROR:" + err);
            }
        }
    });
});