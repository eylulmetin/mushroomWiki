import json
from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

@app.route('/')
def hakkimizda():
    return render_template("index.html")



@app.route('/api/endpoint', methods=['POST'])
def classify_mushroom():
    uploaded_file = request.files['file']
    
    if uploaded_file.filename != '':
        if " " in uploaded_file.filename:
            uploaded_file.filename = "x"
        save_path = os.path.join("static/inputs", uploaded_file.filename)
        uploaded_file.save(save_path)
        filepath = os.path.abspath(save_path)
        
        auth_token_url = "https://iam.ap-southeast-1.myhuaweicloud.com/v3/auth/tokens"
        body = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": "hwc09865700",
                            "password": "Velosipedin4",
                            "domain": {
                                "name": "hwc09865700"
                            }
                        }
                    }
                },
                "scope": {
                    "project": {
                        "name": "ap-southeast-1"
                    }
                }
            }
        }
        
        response = requests.post(auth_token_url, json=body)
        x_auth_token = response.headers["X-Subject-Token"]
        
        service_api_address = "https://e77bab36de434d4bbb37a4b0588b64b9.apigw.ap-southeast-1.huaweicloud.com/v1/infers/6bf3504e-3231-4504-ab76-40d9efb678a8"
        file_path = filepath
        
        headers = {
            'X-Auth-Token': x_auth_token
        }
        
        files = {
            'images': open(file_path, 'rb')
        }
        
        response = requests.post(service_api_address, headers=headers, files=files)
        response_data = json.loads(response.text)
        
        
        predicted_label = response_data["predicted_label"]
       
        
        return jsonify({"mushroom_name": predicted_label})
    
    return jsonify({"error": "Fotoğraf seçtiğinizden emin olun."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)