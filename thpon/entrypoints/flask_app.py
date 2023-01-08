from datetime import datetime
from flask import Flask, jsonify, request
from thpon.domain import commands
# from allocation.service_layer.handlers import InvalidSku
from thpon import bootstrap

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/", methods=["get"])
def hello():
    return "we are here"

@app.route("/add_field/<fid>", methods=["get"])
def create_new(fid):
    cmd = commands.FillInit(fid=fid)
    bus.handle(cmd)
    return "OK", 201


if __name__ == "__main__":
        app.run()
