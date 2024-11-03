from flask import Flask


def hello_world():
    with open('Coffee_map.html', 'r') as html:
        return html.read()


app = Flask(__name__)
app.add_url_rule('/', 'hello', hello_world)
