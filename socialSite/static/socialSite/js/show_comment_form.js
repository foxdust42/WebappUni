window.onload = comment_form_loaded;

function  toggle_comment_form(){
    let comment_form = document.getElementById('comment-form-wrapper');
    if (comment_form.style.display === 'none'){
        comment_form.style.display = "block";
    }
    else {
        comment_form.style.display = "none";
    }
}

function comment_form_loaded(){
    const comment_form = document.getElementById('comment-form-wrapper')
    comment_form.style.display = 'none';
}