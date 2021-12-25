$(document).ready(function(){
    $('#allAnalysis tbody tr').click(function(elm){
        if (elm.target.nodeName == 'A'){
            return;
        } else {
            window.location = $(this).data('href');
            return false;
        }
    });
    if($('#myAnalysis tr').length < 2 ){
        $("table tbody").append("<tr><td colspan='7' style='text-align:center'>No analysis yet</td></tr>");
    }
  });