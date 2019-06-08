// 清空聊天记录
var clear_board = function()
{
    var chat_area = document.querySelector('#id-chat-area')
    chat_area.value = ''
}

var socket;

// 初始化 websocket 的连接
var socket_startup = function() {
    var url = 'ws://' + document.domain + ':' + location.port + '/chat'
    window.socket = io.connect(url);
    window.socket.on('connect', function() {
        console.log('connect', url);
        // log('compare socket', socket.id, window.socket.id)
        clear_board();
    });
}

// 按下回车键，发送消息
var bindKeySubmit = function() {
    log('socket enter func', window.socket)
    document.addEventListener('keydown', function(event) {
        var key = event.key
        var text = document.querySelector('#id-text')
        if (key == 'Enter') {
            // log('text', text.value)
            var data = {text: text.value}
            s = window.socket.emit('event_text', data)
            log('data sent:', data)
            text.value = ''

        }
    });
}

var socket_recv_message = function() {
    window.socket.on('event_text', function(data) {
        log('response of socket', data)
        var chat_area = document.querySelector('#id-chat-area')
        var append_text = data.text + '\n'
        chat_area.value += append_text
    });
}

var _main = function() {
    socket_startup()
    bindKeySubmit()
    socket_recv_message()

}

_main()
