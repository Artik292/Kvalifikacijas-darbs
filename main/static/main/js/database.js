var modalityTable = $('#modality');
var descriptionTable = $('#description');
var patient_idTable = $('#patient_id');
var sexTable = $('#sex');

$('tr').click(function(){
    var modality = $(this).find('.modality').text();
    var discription = $(this).find('.description').text();
    var patient_id = $(this).find('.patient_id').text();
    var sex = $(this).find('.sex').text();
    modalityTable.text(modality);
    descriptionTable.text(discription);
})