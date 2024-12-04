from http import HTTPStatus
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger

from dotenv import load_dotenv

load_dotenv()

from adapters.http import payment_api

app = Flask("FoodAPI")
CORS(app)
swagger = Swagger(app)

BASE_PATH = "/api/v1"

app.register_blueprint(payment_api, url_prefix=BASE_PATH)


app.json.sort_keys = False


@app.get("/")
def root():
    return jsonify({"project": "Tech Challence - Fase 4"}), HTTPStatus.OK


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
