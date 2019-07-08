from app import (
    configured_app,
    socketio,
)
# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # config = dict(
    #     debug=True,
    #     host='127.0.0.1',
    #     port=2000,
    # )

    # 启动
    app = configured_app()
    # app.run(**config)
    # socketio.run(app, host='127.0.0.1', port=2000, debug=True)
    socketio.run(app, debug=True)
