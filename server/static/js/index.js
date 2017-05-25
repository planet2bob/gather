var messages = [{
    'message': 'HEY BIDEN',
    'sender': 'some-guy',
    'source': 'slack',
    'recipient': 'Joe "Daddy" Biden'
}];

var canMerge;
var c1;
var c2;
var socket = io.connect('http://' + document.domain + ':' + location.port, { 'sync disconnect on unload': true });

socket.on('num_users', function(num) {
    console.log('num-users: ' + num);
});

socket.on('id', function(id) {
    console.log('id: ' + id);
})
socket.on('contacts', function(data) {
    console.log(data);
    renderContacts(data);
});
socket.on('message', function(data) {
    console.log(data);
    messages.push(data);
    renderMessages();
});

function getContacts() {
    socket.emit('contacts');
}

function renderContacts(contacts) {

    //<li class="panel panel-info list-group-item justify-content-between contact text-primary" id="max-skype">max
    //<span class="btn-group pull-right edit-button">
        //<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
            //<span class="fa fa-pencil-square-o"></span>
        //</button>

        //<ul class="dropdown-menu" role="menu">
            //<li class="open-edit-name-modal" data-toggle="modal" data-target="#edit-name-modal" data-id="max-skype">
                //<a>Edit name</a>
            //</li>

            //<li class="delete-convo" data-id="max-skype">
                //<a>Delete conversation</a>
            //</li>
        //</ul>
    //</span>
    //</li>

    var contactList = document.getElementById("contact-list");

    for (i = 0; i < contacts.length; i++) {

        var contactName = contacts[i].username;
        var contactService = contacts[i].service;
        var contactId = contactName + '-' + contactService;
        

        var row = document.createElement('li');
        if (i == 0) {
            row.className = "panel panel-info list-group-item justify-content-between active contact text-primary";
        }
        else {
            row.className = "panel panel-info list-group-item justify-content-between contact text-primary";
        }
        row.id = contactId;

        row.innerText = contactName;

        var dropdown = document.createElement('span');
        dropdown.className = "btn-group pull-right edit-button";

        var editButton = document.createElement('button');
        editButton.type = "button";
        editButton.className = "btn btn-default dropdown-toggle";
        editButton.setAttribute('data-toggle' , 'dropdown');
        //editButton.data-toggle = "dropdown";

        var editIcon = document.createElement('span');
        editIcon.className = "fa fa-pencil-square-o";
        editButton.appendChild(editIcon);

        dropdown.appendChild(editButton);
       
        var menu = document.createElement('ul');
        menu.className = 'dropdown-menu';
        menu.setAttribute('role', 'menu');


        var editName = document.createElement('li');
        editName.className = "open-edit-name-modal";
        editName.setAttribute('data-toggle', 'modal');
        editName.setAttribute('data-target', '#edit-name-modal');
        editName.setAttribute('data-id', contactId);

        var text = document.createElement('a');
        text.innerText = "Edit name";
        editName.appendChild(text);

        menu.appendChild(editName);

        var deleteConvo = document.createElement('li');
        deleteConvo.className = "delete-convo";
        deleteConvo.setAttribute('data-id', contactId);

        var text2 = document.createElement('a');
        text2.innerText = "Delete conversation";
        deleteConvo.appendChild(text2);

        menu.appendChild(deleteConvo);

        dropdown.appendChild(menu);  

        row.appendChild(dropdown);

        contactList.appendChild(row);

    }

    console.log(contactList.innerHTML);

}

//getContacts();

// document.getElementById('submit').onclick = function() {
//     var username = document.getElementById('user').value;
//     var password = document.getElementById('pass').value;
//     socket.emit('acc_info', {
//         username: username,
//         password: password
//     });
// }



// window.onbeforeunload = function() {
//     socket.emit('dc');
//     console.log('!');
// }

function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    } else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

console.log(readCookie('id'));

var sortables = $(".contact");
var draggedItem;

$("#contact-list").sortable({
    start: function(event, ui) {
        draggedItem = ui.item;
        $(window).mousemove(moved);
    },
    stop: function(event, ui) {
        $(window).unbind("mousemove", moved);
    }
});

function moved(e) {
    canMerge = false;
    c1 = "";
    c2 = "";
    //Dragged item's position++
    var dpos = draggedItem.position();
    var d = {
        top: dpos.top,
        bottom: dpos.top + draggedItem.height(),
        left: dpos.left,
        right: dpos.left + draggedItem.width()
    };

    //Find sortable elements (li's) covered by draggedItem
    var hoveredOver = sortables.not(draggedItem).filter(function() {
        var t = $(this);
        var pos = t.position();

        //This li's position++
        var p = {
            top: pos.top,
            bottom: pos.top + t.height(),
            left: pos.left,
            right: pos.left + t.width()
        };

        //itc = intersect
        var itcTop = p.top <= d.bottom;
        var itcBtm = d.top <= p.bottom;
        var itcLeft = p.left <= d.right;
        var itcRight = d.left <= p.right;

        return itcTop && itcBtm && itcLeft && itcRight;
    });

    hoveredOver.each(function() {
        // draggedItemName = draggedItem.text().replace('Edit name', '').replace('Delete conversation', '').trim();
        // hoveredOverName = this.textContent.replace('Edit name', '').replace('Delete conversation', '').trim();
        canMerge = true;
        c1 = draggedItem.attr('id');
        c2 = this.id;

    });
};



$(".contact").mouseup(function() {
    if ((canMerge) && (c1 != "") && (c2 != "")) {
        mergeContacts(c1, c2);
    }
});

function mergeContacts(c1, c2) { // args are contact id's

    if (confirm("Are you sure you want to merge these two contacts?")) {
        console.log("MERGING CONTACTS " + c1 + " and " + c2);
        console.log("THIS SHOULD MERGE " + c1 + " AND " + c2 + " IN THE DATABASE");
        //way more frontend display of messages needed, but that'll happen once render messages is done
        $('#' + c2).remove();
    } else {

    }
    canMerge = false;
}

$(document).on("click", ".delete-convo", function() {
    if (confirm("Do you want to delete this conversation?")) {
        var contactId = $(this).data('id');
        console.log("THIS SHOULD DELETE CONVERSATION OF " + contactId + " FROM DATABASE");
        $('#' + contactId).remove();
    } else {

    }
});


//show edit button on hover
$('.contact').hover(function() {
        $(this).find(".edit-button").show();
    },
    function() {
        $(this).find(".edit-button").hide();
    }
);


$('.contact').click(function() {
    console.log('changing contacts...');
    var contactButtons = document.getElementsByClassName('contact');
    for (var i = 0; i < contactButtons.length; i++) {
        $(contactButtons[i]).removeClass('active');
    }
    $(this).addClass('active');
    renderMessages();
});

$(document).on("click", ".open-edit-name-modal", function() {
    var contactId = $(this).data('id');
    $(".modal-body #current-name").val(contactId);

});

$('#save-name-btn').click(function() {
    console.log('saving name...');
    var newName = document.getElementById('recipient-name').value;
    document.getElementById('recipient-name').value = "";
    console.log("New name: " + newName);

    contactId = "#" + $(".modal-body #current-name").val();
    console.log(contactId);

    contactChildren = $(contactId).children();
    $(contactId).text(newName);
    $(contactId).append(contactChildren);

    console.log("THIS SHOULD SAVE NEW NAME " + newName + " TO DATABASE.");

    $('#edit-name-modal').modal('hide');

});

function renderMessages() {
    var activeContact = $('.active').text();
    document.getElementById('messages-box').innerHTML = "";
    for (var i = 0; i < messages.length; i++) {
        if (messages[i].sender === activeContact) {
            var row = document.createElement('div');
            row.class = "row";
            var message = document.createElement('div');
            message.className = "received-message alert alert-success col-sm-9 pull-left";
            var text = document.createElement('p');
            text.innerText = messages[i].message;
            message.appendChild(text);
            var h6 = document.createElement('h6');
            h6.className = "signature pull-right text-muted";
            h6.innerText = messages[i].sender + ' ';
            var logoSpan = document.createElement('span');
            logoSpan.className = "fa fa-" + messages[i].source;
            h6.appendChild(logoSpan);
            message.appendChild(h6);
            row.appendChild(message);
            $('#messages-box').append(row);
            $('#messages-box').scrollTop($('#messages-box')[0].scrollHeight);
        } else if (messages[i].recipient === activeContact) {
            var row = document.createElement('div');
            row.class = "row";
            var message = document.createElement('div');
            message.className = "sent-message alert alert-success col-sm-9 pull-right";
            var text = document.createElement('p');
            text.innerText = messages[i].message;
            message.appendChild(text);
            var h6 = document.createElement('h6');
            h6.className = "signature pull-right text-muted";
            h6.innerText = messages[i].sender + ' ';
            var logoSpan = document.createElement('span');
            logoSpan.className = "fa fa-" + messages[i].source;
            h6.appendChild(logoSpan);
            message.appendChild(h6);
            row.appendChild(message);
            $('#messages-box').append(row);
            $('#messages-box').scrollTop($('#messages-box')[0].scrollHeight);
        }
    }

}

$('.sendmethod').click(function() {
    var method = this.id;
    document.getElementById('currentplatform').className = "fa fa-" + method;
});

$('.add-platform-method').click(function() {
    var method = this.id;
    document.getElementById('add-platform').className = "fa fa-" + method;
});

$("#own-message").keyup(function(event) {
    if (event.keyCode == 13) {
        var val = $('#own-message').val();
        var method = document.getElementById('currentplatform').className.substring(6);
        var messageData = {
            message: val,
            sender: 'maxsun',
            source: method,
            recipient: $('.active').text()
        };
        $('#own-message').val('');
        renderMessages();
        // $.ajax({
        //     type: "POST",
        //     url: '/send',
        //     data: messageData,
        //     success: function (d) {
        //         messages.push(messageData);
        //     },
        //     dataType: "JSON"
        // });
        socket.emit('send', {
            'message': val,
            'method': method,
            'recipient': $('.active').text()
        });
    }
});