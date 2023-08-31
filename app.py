import os

from flask import Flask

from core.ws_spam_model_updater.api import urls_blueprint
from core.ws_spam_model_updater.swagger_docs.swagger_config import (
    SWAGGER_URL, swaggerui_blueprint)

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(urls_blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port,debug=False)
