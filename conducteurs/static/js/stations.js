$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-station').modal('show');
            },
            success: function(data){
                $('#modal-station .modal-content').html(data.html_form);
            }
        });
    };
    var SaveForm = function() {
        var form = $(this);
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data) {
                if(data.form_is_valid) {
                    $('#dataTable tbody').html(data.station);
                    $('#modal-station').modal('hide');
                } else {
                    $('#modal-station .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-station').on("submit", ".create-form", SaveForm);

// Update form
$('#dataTable').on("click", ".show-form-update", ShowForm);
$('#modal-station').on("submit", ".update-form", SaveForm);

// Delete form
$('#dataTable').on("click", ".show-form-delete", ShowForm);
$('#modal-station').on("submit", ".delete-form", SaveForm);

});