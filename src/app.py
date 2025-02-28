from flask import Flask
from api.routes import configure_routes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
configure_routes(app)

if __name__ == "__main__":
    app.run(debug=False)