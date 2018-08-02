$( document ).ready(function() {
    console.log( "ready!" );
});

$("#submitForm").click(function(event) {
        event.preventDefault();
        $("#translate-form").submit();
        console.log('submitted');
		
});

// $(outputlang).val($(outputlang).val() + 'hello')

function myFunc(vars) {
    return vars
}
