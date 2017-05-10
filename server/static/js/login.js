console.log('login js!');

var socket = io.connect('http://' + document.domain + ':' + location.port, { 'sync disconnect on unload': true });

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

$('#submitLogin').on('click', function() {
    var email = $('#email').val();
    var password = $('#pwd').val();
    socket.emit('login', {
        password: password,
        username: email
    });
});

$('#submitRegister').on('click', function() {
    var email = $('#email').val();
    var password = $('#pwd').val();
    socket.emit('register', {
        password: password,
        username: email
    });
});

socket.on('refresh', function(id) {
    console.log('fake refreshing...');
    console.log(id);
    eraseCookie('id');
    createCookie('id', id, 1);
    document.cookie = 'id=' + id;
    window.location = '/';
});