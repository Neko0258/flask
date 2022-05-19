from flask import Flask
from dbconfig import app


if __name__ == "__main__":
    app.run(debug=True, port="3000")