(function () {
    var template = document.querySelector("template").content;
    var chat_messages = document.querySelector(".chat_messages");
    var first_child = document.querySelector(".first_child");
    var create_message = function (element) {
        var operation_element = template.cloneNode(true);
        var message = operation_element.querySelector('.message')
        message.textContent = element.username + ": " + element.message + '\n' + element.datetime
        return operation_element
    }
    const chat_id = JSON.parse(document.getElementById('chat-id').textContent);
    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + chat_id
        + "/"
    );

    function insertAfter(newNode, existingNode) {
        existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        // document.querySelector('#chat-log').value += (data.username + ": " + data.message + "\n")
        var fragment = document.createDocumentFragment();
        fragment.appendChild(create_message(data))
        insertAfter(fragment, first_child)
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };

    document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
})()
