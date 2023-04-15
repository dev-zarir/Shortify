from server import init_app

app = init_app(__name__, ver=2.3)

if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)

