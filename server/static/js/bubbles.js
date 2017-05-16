function displayMessage(text) {
    var message = document.createElement("div");

    message.style.margin = "40px";
    message.style.display = "inline-block";
    message.style.position = "relative";
    message.style.width = "200px";
    message.style.height = "50px";
    message.style.backgroundColor = "lightyellow";
    message.innerHTML = text;
    message.style.padding = "1em";
    message.style.textAlign = "left";
    message.style.lineHeight = "1.5em";
    message.style.position = "relative"

    document.getElementById("2").appendChild(message);
}

(function () {
    var Message;
    Message = function (arg) {
        console.log(arg.text);
        this.text = arg.text, this.message_side = arg.message_side;
        this.draw = function (_this) {
            return function () {
                var $message;
                $message = $($('.message_template').clone().html());
                $message.addClass(_this.message_side).find('.text').html(_this.text);
                $('.messages').append($message);
                return setTimeout(function () {
                    return $message.addClass('appeared');
                }, 0);
            };
        }(this);
        return this;
    };
    $(function () {
        var getMessageText, message_side, sendMessage;
        message_side = 'right';
        getMessageText = function () {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function (text) {
            var $messages, message;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message_side = 'right';
            message = new Message({
                text: text,
                message_side: message_side
            });
            message.draw();
            return $messages.animate({
                scrollTop: $messages.prop('scrollHeight')
            }, 300);
        };
        $('.send_message').click(function (e) {
            return sendMessage(getMessageText());
        });
        $('.message_input').keyup(function (e) {
            if (e.which === 13) {
                return sendMessage(getMessageText());
            }
        });
    });
}.call(this));
