$(document).ready(function(){
    // when doctors click on table row with all analyzes, this funtion follows the link on rows href attribute
    $('#allAnalysis tbody tr').click(function(elm){
        if (elm.target.nodeName == 'A'){
            return;
        } else {
            window.location = $(this).data('href');
            return false;
        }
    });
    $('#MyAnalysis tbody tr').click(function(elm){
        if (elm.target.nodeName == 'A'){
            return;
        } else {
            window.location = $(this).data('href');
            return false;
        }
    });
    // if doctor's tables with analyzes are empty this scripts appends row with text relevant text
    if($('#MyAnalysis tr').length < 2 ){
        $("#MyAnalysis tbody").append("<tr><td colspan='9' style='text-align:center'>No analyzes yet</td></tr>");
    }
    if($('#allAnalysis tr').length < 2 ){
        $("#allAnalysis tbody").append("<tr><td colspan='9' style='text-align:center'>No analyzes yet</td></tr>");
    }
  });