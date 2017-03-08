var messages = [{
    'message': 'HEY BIDEN',
    'sender': 'some-guy',
    'source': 'slack',
    'recipient': 'Joe "Daddy" Biden'
}];
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    console.log('connected!');
    socket.emit('connected', {
        username: 'maxsun',
        password: 'abcd'
    });
});

var canMerge;
var c1;
var c2;

$(function() {

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
            bottom:    dpos.top + draggedItem.height(),
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
                bottom:    pos.top + t.height(),
                left: pos.left,
                right: pos.left + t.width()
            };

            //itc = intersect
            var itcTop         = p.top <= d.bottom;
            var itcBtm         = d.top <= p.bottom;
            var itcLeft     = p.left <= d.right;
            var itcRight     = d.left <= p.right;

            return itcTop && itcBtm && itcLeft && itcRight;
        });

        hoveredOver.each(function() {
            // draggedItemName = draggedItem.text().replace('Edit name', '').replace('Delete contact', '').trim();
            // hoveredOverName = this.textContent.replace('Edit name', '').replace('Delete contact', '').trim();
            canMerge = true;
            c1 = draggedItem.attr('id');
            c2 = this.id;

        });
    };

});


$(".contact").mouseup(function(){
    if ( (canMerge) && (c1 != "") && (c2 != "") ){
        mergeContacts(c1, c2);
    }
});

function mergeContacts(c1, c2) { // args are contact id's
    console.log("MERGING CONTACTS " + c1 + " and " + c2);
    //way more display of messages needed, but that'll happen once render messages is done
    $('#'+c2).remove();
}

$(document).on("click", ".delete-contact", function () {
    var contactId = $(this).data('id');
    console.log("THIS SHOULD DELETE " + contactId + " FROM DATABASE");
    $('#'+contactId).remove();
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

$(document).on("click", ".open-edit-name-modal", function () {
    var contactId = $(this).data('id');
    $(".modal-body #current-name").val( contactId );

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

    //prints to console that it should save to database
    console.log("This SHOULD save new name to database.");

    $('#edit-name-modal').modal('hide');

})


function renderContacts() {
    return;
}


socket.on('status', function (data) {
    console.log(data);
});

socket.on('message', function (data) {
    console.log(data);
    messages.push(data);
    renderMessages();
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

$("#own-message").keyup(function(event){
    if(event.keyCode == 13){
        var val = $('#own-message').val();
        var method = document.getElementById('currentplatform').className.substring(6);
        var messageData = {
            message : val,
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

function requestMessages() {
    socket.emit('get', {
        username: 'maxsun',
        password: 'abcd'
    });
}

window.setInterval(function(){
    requestMessages();
}, 5000);

renderMessages();