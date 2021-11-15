$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-droit').modal('show');
            },
            success: function(data){
                $('#modal-droit .modal-content').html(data.html_form);
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
                    $('#dataTable tbody').html(data.droit);
                    $('#modal-droit').modal('hide');
                } else {
                    $('#modal-droit .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-droit').on("submit", ".create-form", SaveForm);

// Update form
$('#dataTable').on("click", ".show-form-update", ShowForm);
$('#modal-droit').on("submit", ".update-form", SaveForm);

// Delete form
$('#dataTable').on("click", ".show-form-delete", ShowForm);
$('#modal-droit').on("submit", ".delete-form", SaveForm);

});