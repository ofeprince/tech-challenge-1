from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)

# Configuration of Swagger
app.config['SWAGGER'] = {
    'title': 'My flask API',
    'uiversion': 3
}
# /apidocs/
swagger = Swagger(app)

# This annotation defines a route
@app.route('/')
def home():
    return "Hello, world!"

# Run the application
# __name__ is a special built-in variable defined by Python
if __name__ == '__main__':
    app.run(debug = True)