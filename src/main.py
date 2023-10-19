import logging

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_file

from tools.reply_user import ReplyUser

load_dotenv("/app/.env")

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
agent = ReplyUser(verbose=False)

def get_completion(prompt):
    return agent.reply_user(prompt)


@app.route("/", methods=["POST", "GET"])
def query_view():
    if request.method == "POST":
        logging.info("step1")
        prompt = request.form["prompt"]
        response = get_completion(prompt)
        logging.info(response)

        return jsonify({"response": response})
    return render_template("index.html")


@app.route('/lat.png')
def serve_image():
    filename = 'lat.png'
    return send_file(f'/app/lat.png', mimetype='image/png')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
