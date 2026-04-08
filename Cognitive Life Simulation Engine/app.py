from flask import Flask, jsonify, render_template
import simulation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start")
def start():
    simulation.init_simulation()
    return jsonify({"status": "started"})


@app.route("/step")
def step():
    data = simulation.step_simulation()

    if not data:
        return jsonify({})

    agents_data = [
        {
            "name": a.name,
            "emotion": a.emotion,
            "stress": a.stress
        }
        for a in simulation.agents
    ]

    return jsonify({
        "logs": data["logs"],
        "agents": agents_data
    })


@app.route("/stop")
def stop():
    simulation.stop_simulation()
    return jsonify({"status": "stopped"})


if __name__ == "__main__":
    app.run(debug=True)