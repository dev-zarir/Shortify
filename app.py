from flask import Flask, request
from routes import endpoints
from urllib.parse import urlsplit

app = Flask(__name__)

@app.context_processor
def contexts():
    def esc_url(url:str):
        url_path = urlsplit(url).path + '?' + urlsplit(url).query if urlsplit(url).query else urlsplit(url).path
        url = request.url_root[:-1] + url_path if request.url_root.endswith('/') else request.url_root + url_path
        return url

    return dict(esc_url=esc_url)

app.register_blueprint(endpoints, url_prefix='/')

if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)

