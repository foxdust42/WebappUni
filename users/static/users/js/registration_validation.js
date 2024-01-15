
//This checks if a username is already taken for client side validation. The server does it on its own end
//once it receives a submitted form
let uname_changed = false;
$(document).ready(function(){
    //create ajax call
    $('#id_username').keyup(function (){
        let taken_msg = "This username is already taken, please choose another one."
        if(!uname_changed){
            clear_all_errors($('#id_username')[0].id);
            uname_changed = true;
        }
        $.ajax({
            data: $(this).serialize(),
            url: $('#validator-ref').prop("value"),
            success: function (response){
                //console.log("A");
                //console.log(response.is_taken);
                const username_field = $('#id_username');
                if(response.is_taken){
                    username_field[0].setCustomValidity(taken_msg);
                    display_custom_error(username_field[0].id, "error_username_taken", taken_msg);
                }
                else {
                    username_field[0].setCustomValidity("");
                    kill_custom_error("error_username_taken");
                }
            },
            error: function (response) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})

//handles client side email validation
let email_changed = false;
$(document).ready(function (){
    $('#id_email').keyup(function (){
        let email_field = $('#id_email');
        if(!email_changed){
            clear_all_errors(email_field[0].id);
            uname_changed = true;
        }
        const msg = "Please enter a valid email";
        //I am not doing quoted strings
        //why is email this complicated
        const email_regex = /^([A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+\.)*([A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+)+@([A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+\.)+(?![0-9]+$)[A-Za-z0-9!#$%&'*+\-/=?^_`{|}~]+$/
        if (!email_regex.test(email_field[0].value)){
            email_field[0].setCustomValidity(msg);
            display_custom_error(email_field[0].id, "error_invalid_email", msg);
        }
        else {
            email_field[0].setCustomValidity("");
            kill_custom_error("error_invalid_email");
        }
    });
})

//I'm leaving strength and username/email similarity to server
//This leaves me to check if it's longer than/equal to 8 and if its fully numeric
$(document).ready(function (){
    $('#id_password1').keyup(function (){
       let pass_field = $('#id_password1');
       const num_regex = /^[0-9]+$/;
       const msg_short = "The password must be at leas 8 characters long"
       const msg_num = "The password may not be only numeric";
       pass_field[0].setCustomValidity("");
       if (pass_field[0].value.length < 8){
           pass_field[0].setCustomValidity("Password too short");
           display_custom_error(pass_field[0].id, "error_pass_too_short", msg_short);
       }
       else {
           kill_custom_error("error_pass_too_short");
       }
       if (num_regex.test(pass_field[0].value)){
           pass_field[0].setCustomValidity("Password may not be only numeric");
           display_custom_error(pass_field[0].id, "error_pass_numeric", msg_num);
       }
       else{
           kill_custom_error("error_pass_numeric");
       }
       $('#id_password2').keyup();
    });
})

let pass_change = false;
$(document).ready( function (){
    $('#id_password2').keyup(function (){
        let pass_org = $('#id_password1');
        let pass_rep = $('#id_password2');
        if(!pass_change){
            clear_all_errors(pass_rep[0].id);
            pass_change = true;
        }
        const msg = "The passwords must match";
        if (pass_org[0].value !== pass_rep[0].value){
            pass_rep[0].setCustomValidity("Passwords must match");
            display_custom_error(pass_rep[0].id, "error_pass_mismatch", msg);
        } else {
          kill_custom_error("error_pass_mismatch");
          pass_rep[0].setCustomValidity("");
        }
    });
})

//Used to clear errors from server once user starts changing things
function clear_all_errors(issuer_id){
    let errorlist = document.getElementById("errorlist_"+issuer_id);
    while (errorlist.firstChild){
        errorlist.lastChild.remove();
    }
}

//For nice client-side errors. Sever will also scream at you if enter something incorrectly, so its purely for usability
function display_custom_error(issuer_id, error_id, msg){
    let err = document.getElementById(error_id);
    if (err != null){
        err.value = msg;
    }
    else {
        console.log(issuer_id);
        let errorlist = document.getElementById("errorlist_"+issuer_id);
        let error = document.createElement('li');
        error.id = error_id;
        error.appendChild(document.createTextNode(msg));
        errorlist.appendChild(error);
    }
}
function kill_custom_error(id){
    let err = document.getElementById(id);
    if (err != null){
        err.remove();
    }
}