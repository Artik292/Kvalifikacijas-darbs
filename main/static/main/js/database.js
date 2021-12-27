$(document).ready(function(){
    $('#allAnalysis tbody tr').click(function(elm){
        if (elm.target.nodeName == 'A'){
            return;
        } else {
            window.location = $(this).data('href');
            return false;
        }
    });
    if($('#MyAnalysis tr').length < 2 ){
        $("#MyAnalysis tbody").append("<tr><td colspan='9' style='text-align:center'>No analysis yet</td></tr>");
    }
    if($('#tableDatabase tr').length < 2 ){
        $("#tableDatabase tbody").append("<tr><td colspan='9' style='text-align:center'>No analysis yet</td></tr>");
    }
  });