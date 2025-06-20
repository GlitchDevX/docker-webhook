from flask import Flask, request, jsonify, abort
from src.docker_connector import redeploy_container

app = Flask(__name__)

@app.route('/trigger-docker-redeploy', methods=['POST'])
def webhook_receiver():

    if not secret_matches(request.headers):
        abort(403)

    data = request.json

    print("Received webhook data:", data)

    if "image" not in data:
        abort(400, "Missing Argument: image")


    redeploy_container(data["image"])

    return jsonify({'message': 'Webhook received successfully'}), 200


def secret_matches(headers) -> bool:
    if "X-Api-Secret" not in headers.keys():
        return False

    return headers["X-Api-Secret"] == "_>?gIESld2$9K|kkPEwzd/@WBqN3)=T3S(b_3r)$>Z%!B0@uQp" # test api key

if __name__ == '__main__':
    app.run(debug=True)

