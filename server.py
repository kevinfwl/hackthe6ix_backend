from flask import Flask
from flask import request
from flask import jsonify
import azureAI
import requests

app = Flask(__name__)

TorontoAvgSize = 1250
neighbourhoodsInToronto =  {
    "Don Valley Village":586,
    "Etobicoke":733,
    "Harbourfront":778,
    "Bayview Village" : 860,
    "Scarborough": 864,
    "Willowdale:": 877,
    "Eringate:": 915,
    "Don Mills:": 928,
    "Bathurst Manor": 992,
    "Downsview": 1029,
    "Rexdale": 1084,
    "Jane and Finch" : 1095,
    "Weston": 1213,
    "Woodbine Heights": 1259,
    "Financial District": 1414,
    "Eglinton West": 1447,
    "High Park": 1456,
    "York Mills": 1587
}

@app.route('/')
def hello_world():
    return 'back end running'

# claim object goes like 
# [
#     houseSize,
#     Address,
#     YearActive,
#     [name, BeforePic, AfterPic ]
#     ...
# ]

@app.route("/claim", methods=['POST'])
def postClaim():
    totalClaims = 0
    obj = { "houseCost" : 1214504.12 }
    for claim in request.json["assets"]:
        calculatedCost = azureAI.findCostDifference(claim, 51.3)
        obj["assets"].append(calculatedCost)
        totalClaims = totalClaims + calculatedCost["claimAmount"]
    obj["totalClaims"] = totalClaims
    return jsonify(obj), 201


@app.route("/securityGrants", methods=["POST"])
def postSecurity():
    return "hi"
