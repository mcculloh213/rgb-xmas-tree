import os
from flask import Flask, jsonify, request

app = Flask(__name__)
STATE_DIR = "/home/pi/xmas"
CONTEXT = {
    "state": "off",
    "mode": "static",
    "brightness": 0.5,
    "r": 255,
    "g": 255,
    "b": 255,
    "period": 2.5,
}


def __init():
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)
    __load_context()


def __load_context():
    try:
        from json import load

        with open(os.path.join(STATE_DIR, "context.json"), "r") as f:
            CONTEXT.update(load(f))
    except FileNotFoundError:
        __put_context()


def __put_context():
    try:
        from json import dump

        with open(os.path.join(STATE_DIR, "context.json"), "w") as f:
            dump(CONTEXT, f)
    except IOError:
        pass


@app.route("/", methods=["GET"])
def index():  # put application's code here
    return "Hello World!"


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return {}


@app.route("/api/v1/context", methods=["GET"])
def get_context():
    """Get the current operational context."""
    return jsonify(**CONTEXT), 200


@app.route("/api/v1/state", methods=["GET"])
def get_state():
    """Get the current operational state."""
    return jsonify(state=CONTEXT.get("state", "???")), 200


@app.route("/api/v1/state/on", methods=["PUT"])
def put_state_on():
    """Turn the NeoPixel LEDs on."""
    CONTEXT.update({"state": "on"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/state/off", methods=["PUT"])
def put_state_off():
    """Turn the NeoPixel LEDs off."""
    CONTEXT.update({"state": "off"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/mode/static", methods=["PUT"])
def put_mode_static():
    """Set the light mode to static."""
    CONTEXT.update({"mode": "static"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/mode/dynamic", methods=["PUT"])
def put_mode_dynamic():
    """Set the light mode to dynamic."""
    CONTEXT.update({"mode": "dynamic"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/mode/rgb", methods=["PUT"])
def put_mode_rgb():
    """Set the light mode to rgb."""
    CONTEXT.update({"mode": "rgb"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/mode/linear", methods=["PUT"])
def put_mode_linear():
    """Set the light mode to linear."""
    CONTEXT.update({"mode": "linear"})
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/brightness", methods=["PUT"])
def put_brightness():
    """Set the brightness."""
    CONTEXT.update(
        {"brightness": min(request.args.get("b", default=0.5, type=float), 1.0)}
    )
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/color", methods=["PUT"])
def put_color():
    """Set the color. [0, 255] => RGB; -1 => random.random()"""
    color = {
        "r": min(request.args.get("r", default=-1, type=int), 255),
        "g": min(request.args.get("g", default=-1, type=int), 255),
        "b": min(request.args.get("b", default=-1, type=int), 255),
    }
    CONTEXT.update(**color)
    __put_context()
    return jsonify(), 201


@app.route("/api/v1/period", methods=["PUT"])
def put_period():
    """ Set the sleep interval in-between context checks (in seconds). """
    CONTEXT.update({"period": min(abs(request.args.get("p", default=2.5, type=float)), 30.0)})
    __put_context()
    return jsonify(), 201


__init()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
