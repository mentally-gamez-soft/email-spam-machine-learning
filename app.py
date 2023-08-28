# from core.ws_spam_checker import api
from core.ws_spam_model_updater import create_app
import os

# app.run(host="192.168.0.14",debug=True)
# api.web_service_api.run(debug=True)

# api.web_service_api.run(host="0.0.0.0",port=5000,debug=False)
 

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port,debug=False)
