import os

from flask import Flask

from core.ws_spam_model_updater.api import urls_blueprint

app = Flask(__name__)
app.register_blueprint(urls_blueprint)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port,debug=False)
