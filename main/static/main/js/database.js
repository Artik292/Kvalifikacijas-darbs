$(document).ready(function(){
    $('#allAnalysis tbody tr').click(function(elm){
        if (elm.target.nodeName == 'A'){
            return;
        } else {
            window.location = $(this).data('href');
            return false;
        }
    });
  });