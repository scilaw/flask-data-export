$(document).ready(function() {

    $('.nav-tabs a').click(function(e) {
        e.preventDefault();
        $('div.flashes').remove();
        $(this).tab('show');
    })

    $('.nav-tabs a:first').tab('show');

    $('select.select_vars').multiselect({
        includeSelectAllOption: true
    });

    $('select.filter_vars').multiselect({
        includeSelectAllOption: true
    });

});
