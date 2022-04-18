from flask.cli import FlaskGroup

from app import app

server = FlaskGroup(app)

if __name__ == "__main__":
    server()
