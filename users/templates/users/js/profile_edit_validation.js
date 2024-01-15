function profile_edit_validation(e){
    //check image extension
    const allowed_extensions =  ["png", "svg", "jpeg", "jpg", "webp"];
    let img = document.getElementById('id_profile_picture');
    let ind = img.lastIndexOf(".");
    let ext = img.value.substring(ind+1);
    if (allowed_extensions.indexOf(ext) === -1){
        //invalid type
        img.setCustomValidity("The provided image has an invalid type. Please submit another image");
    }
    else {
        img.setCustomValidity("");
    }
}

function clear_image(){
    let e = document.getElementById('id_profile_picture');
    e.value = "";
}