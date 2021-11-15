$(document).ready(function(){
    var ShowForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-utilisateur').modal('show');
            },
            success: function(data){
                $('#modal-utilisateur .modal-content').html(data.html_form);
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
                    $('#table-utilisateur tbody').html(data.utilisateur);
                    $('#modal-utilisateur').modal('hide');
                } else {
                    $('#modal-utilisateur .modal-content').html(data.html_form);
                }
            }
        })
        return false;
    };

// Create a form
$(".show-form").click(ShowForm);
$('#modal-utilisateur').on("submit", ".create-form", SaveForm);

// Update form
$('#table-utilisateur').on("click", ".show-form-update", ShowForm);
$('#modal-utilisateur').on("submit", ".update-form", SaveForm);

// Delete form
$('#table-utilisateur').on("click", ".show-form-delete", ShowForm);
$('#modal-utilisateur').on("submit", ".delete-form", SaveForm);

// Delete form
$('#table-utilisateur').on("click", ".show-form-active", ShowForm);
$('#modal-utilisateur').on("submit", ".delete-form", SaveForm);

});