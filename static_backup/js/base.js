function kill_parent_list(e){
    let list = document.getElementById("message-list")
    if (list.children.length === 1) {
        list.remove()
    }
    else {
        e.parentNode.remove()
    }
}