function validateRegisterModal() {
    let message = document.getElementById('r-message');
    let name = document.getElementById("r-name");
    let surname = document.getElementById("r-surname");
    let username = document.getElementById("r-username");
    let password = document.getElementById("r-password");
    let email = document.getElementById("r-email");
    let isValid = true;
    message.innerHTML = "";
    while (true) {
        if (!name.value) {
            name.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide First Name.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else {
            name.style.borderColor = "#ccc";
        }
        if (!surname.value) {
            surname.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Last Name.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else {
            surname.style.borderColor = "#ccc";
        }
        if (!username.value) {
            username.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Username.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else if (username.value.length < 6) {
            username.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Username needs to be at least six (6) characters long.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else if (username) {
            $('document').ready(function() {
                $('form').on('submit', function(e) {
                    e.preventDefault();
                    $.get('/check?username=' + username, function(res) {
                        if (res == false) {
                            username.style.borderColor = "#dc3545";
                            message.innerHTML += "<li>That username is taken.</li>";
                            $('#message-r-div').show();
                            document.getElementById('r-register').reset();
                            $('#username').focus;
                            isValid = false;
                        }
                    });
                });
            });
        } else {
            username.style.borderColor = "#ccc";
        }
        if (!email.value) {
            email.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Email.</li>";
            $('#message-r-div').show();
            isValid = false;
        }
        if (!password.value) {
            password.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Password.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else if (password.value.length < 8) {
            password.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Password needs to be at least eight (8) characters long.</li>";
            $('#message-r-div').show();
            isValid = false;
        } else {
            password.style.borderColor = "#ccc";
        }
        return isValid;
    }
}


function validateLoginModal() {
    let message = document.getElementById('l-message');
    let username = document.getElementById("l-username");
    let password = document.getElementById("l-password");
    let isValid = true;
    message.innerHTML = "";
    while (true) {
        if (!username.value) {
            username.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Username.</li>";
            $('#message-l-div').show();
            isValid = false;
        } else {
            username.style.borderColor = "grey";
        }
        if (!password.value) {
            password.style.borderColor = "#dc3545";
            message.innerHTML += "<li>Must provide Password.</li>";
            $('#message-l-div').show();
            isValid = false;
        } else {
            password.style.borderColor = "grey";
        }
        return isValid;
    }
}


$(document).ready(function() {
    $("#plus").click(function() {
        $(this).fadeOut(1, "swing");
        $("#new-form").fadeIn(1000, "swing");
    });
});

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);

}

function drop(ev) {
    ev.preventDefault();
    var datum = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(datum));
    var status = ev.target.parentElement.id;
    console.log(status);
    document.getElementById(datum).className = "task-list " + status;
    console.log(document.getElementById(datum).id);
    var idx = document.getElementById(datum).id;
    $(document).ready(function() {
        $.ajax({
            data: {
                'new_status': status
            },
            type: 'POST',
            url: '/update/tasks/' + idx
        }).done(function(data) {
            $("#alert").text("Task Updated!");
        });
    });
}

function noAllowDrop(ev) {
    ev.stopPropagation();
}

function name_edit(num) {
    $(document).ready(function() {
        $('#name_task_' + num).hide();
        $('#edit_name_task_' + num).show();
    })
}

function nameUpdate(num) {
    var n = num.toString();
    var form = document.getElementById('edit_name_task_' + n);
    console.log(form);
    var text = document.getElementById('edit_name_' + n);
    console.log(text.value);
    var name = document.getElementById('name_task_' + n);
    console.log(name);
    var view = document.getElementById('new_view_' + n);
    console.log(view);
    name.innerHTML = "<strong>" + text.value + "</strong>";
    view.innerHTML = text.value;
    form.style.display = "none";
    name.style.display = "inline-block";
    console.log(name);

    $(document).ready(function() {
        $.ajax({
            data: {
                'name': text.value
            },
            type: 'POST',
            url: '/update/name/' + n
        }).done(function(data) {
            $("#alert").text("Task Updated!");
        });
    });
}

function desc_edit(num) {
    $(document).ready(function() {
        $('#desc_task_' + num).hide();
        $('#edit_desc_task_' + num).show();
    })
}

function descUpdate(num) {
    var n = num.toString();
    var form = document.getElementById('edit_desc_task_' + n);
    console.log(form);
    var text = document.getElementById('edit_desc_' + n);
    console.log(text.value);
    var desc = document.getElementById('desc_task_' + n);
    console.log(desc);
    desc.innerHTML = text.value;
    form.style.display = "none";
    desc.style.display = "inline-block";
    console.log(desc);

    $(document).ready(function() {
        $.ajax({
            data: {
                'desc': text.value
            },
            type: 'POST',
            url: '/update/desc/' + n
        }).done(function(data) {
            $("#alert").text("Task Updated!");
        });
    });
}

function due_edit(num) {
    $(document).ready(function() {
        $('#due_task_' + num).hide();
        $('#edit_due_task_' + num).show();
    })
}

function dueUpdate(num) {
    var n = num.toString();
    var form = document.getElementById('edit_due_task_' + n);
    console.log(form);
    var text = document.getElementById('edit_due_' + n);
    console.log(text.value);
    var due = document.getElementById('due_task_' + n);
    console.log(due);
    due.innerHTML = text.value;
    form.style.display = "none";
    due.style.display = "inline-block";
    console.log(due);

    $(document).ready(function() {
        $.ajax({
            data: {
                'due': text.value
            },
            type: 'POST',
            url: '/update/due/' + n
        }).done(function(data) {
            $("#alert").text("Task Updated!");
        });
    });
}

function comment_edit(num) {
    $(document).ready(function() {
        $('#comment_text_' + num).hide();
        $('#edit_comment_text_' + num).show();
    });
}

function commentUpdate(num) {
    var n = num.toString();
    var form = document.getElementById('edit_comment_text_' + n);
    console.log(form);
    var text = document.getElementById('comment_edit_' + n);
    console.log(text.value);
    var comment = document.getElementById('comment_text_' + n);
    console.log(comment);
    comment.innerHTML = text.value;
    form.style.display = "none";
    comment.style.display = "inline-block";
    console.log(comment);

    $(document).ready(function() {
        $.ajax({
            data: {
                'text': text.value
            },
            type: 'POST',
            url: '/update/comment/' + n
        }).done(function(data) {
            $("#alert").text("Comment Updated!");
        });
    });
}

function commentDelete(num) {
    var n = num.toString();
    var comment = document.getElementById('commenter_' + n);
    console.log(comment);
    comment.style.display = "none";
    $(document).ready(function() {
        $.ajax({
            data: {
                'idx': num
            },
            type: 'POST',
            url: '/delete/comment'
        }).done(function(data) {
            $("#alert").text("Comment Deleted!");
        });
    });
}