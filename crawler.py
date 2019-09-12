import requests
from bs4 import BeautifulSoup

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

# url = 'https://taqm.epa.gov.tw/pm25/tw/PM25A.aspx?area=10'


@app.route('/')
def select_PM25():
    url = 'https://taqm.epa.gov.tw/pm25/tw/PM25A.aspx?area=10'
    tag = ".TABLE_G"
    tag_location = 'linkSite'
    tag_PM_now = 'lab1'
    tag_PM_record = 'lab2'
    
    res_url = requests.get(url)
    soup = BeautifulSoup(res_url.text, "lxml")

    data = list()
    elem = soup.select('{}'.format(tag))
    for child in elem[0].descendants:
        try:
            tag_id = child.get('id')
        except AttributeError:
            continue

        if not tag_id:
            continue
        if tag_location in tag_id:
            data_local = dict()
            data_local['站名'] = child.text
            data.append(data_local)
        elif tag_PM_now in tag_id:
            data_local['即時濃度'] = child.text
        elif tag_PM_record in tag_id:
            data_local['上一小時濃度'] = child.text
        
        res = {
                'result': True,
                'data': data
                }
    return jsonify(res)
        
if __name__ == "__main__":
    app.run()


