$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-conducteur').modal('show');
            },
            success: function(data){
                $('#modal-conducteur .modal-content').html(data.html_form);
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
                    $('#cdataTable tbody').html(data.conducteur);
                    $('#modal-conducteur').modal('hide');
                } else {
                    $('#modal-conducteur .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-conducteur').on("submit", ".create-form", SaveForm);

// Update form
$('#cdataTable').on("click", ".show-form-update", ShowForm);
$('#modal-conducteur').on("submit", ".update-form", SaveForm);

// Delete form
$('#cdataTable').on("click", ".show-form-delete", ShowForm);
$('#modal-conducteur').on("submit", ".delete-form", SaveForm);

});