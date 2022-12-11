from trashlocation import TrashLocation
from flask import Flask, request
from flask_cors import CORS
from json import dumps
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/",methods = ["POST"])
def locate():
    data_json = request.get_json()
    root_path = os.path.dirname(os.path.abspath(""))
    loc = TrashLocation(root_path=root_path)
    df = loc.get_n_nearest(3, data_json["address"], data_json["trash_type"])
    df.reset_index(inplace=True, drop=True)
    data_response = df.to_dict("index")
    data_list = list(map(lambda x:data_response[x], data_response))
    response = dumps(data_list)
    return response

if __name__ == "__main__":
    app.run(debug=True)
