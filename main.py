from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/trigger-docker-redeploy', methods=['POST'])
def webhook_receiver():

    if not secret_matches(request.headers):
        return 403

    data = request.json
    print("Received webhook data:", data)
    return jsonify({'message': 'Webhook received successfully'}), 200


def secret_matches(headers) -> bool:
    if "X-API-Secret" not in headers.keys():
        return False

    return headers["X-API-Secret"] == "_>?gIESld2$9K|kkPEwzd/@WBqN3)=T3S(b_3r)$>Z%!B0@uQp"

if __name__ == '__main__':
    app.run(debug=True)

