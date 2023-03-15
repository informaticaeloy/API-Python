from uvicorn import Config, Server

server = Server(
    Config(
        "main:app",
        host="127.0.0.1",
        port=9002,
        reload=True,
        log_level='debug' # Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'
    ),
 )

server.run()
