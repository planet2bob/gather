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

$('.contact').click(function() {
    console.log('changing contacts...');
    var contactButtons = document.getElementsByClassName('contact');
    for (var i = 0; i < contactButtons.length; i++) {
        $(contactButtons[i]).removeClass('active');
    }
    $(this).addClass('active');
    renderMessages();
});

socket.on('status', function (data) {
    console.log(data);
});

socket.on('message', function (data) {
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
        $.ajax({
            type: "POST",
            url: '/send',
            data: messageData,
            success: function (d) {
                messages.push(messageData);
            },
            dataType: "JSON"
        });
    }
});

function requestMessages() {
    socket.emit('requestMessages', {
        username: 'maxsun',
        password: 'abcd'
    });
}

window.setInterval(function(){
    requestMessages();
}, 5000);

renderMessages();