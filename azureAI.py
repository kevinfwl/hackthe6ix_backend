from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateEntry
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import base64
import os

ENDPOINT = "https://eastus2.api.cognitive.microsoft.com/"

# Replace with a valid key
training_key = "<your training key>"
prediction_key = "fc16e454671d4f878d14e74bcdc81533"
# prediction_resource_id = "<your prediction resource id>"

publish_iteration_name = "Iteration5"
base_image_url = "<path to project>"
predictor = CustomVisionPredictionClient(prediction_key, endpoint=ENDPOINT)

def predict(name):
    with open("./savedFiles/" + name, "rb") as image_contents:
        results = predictor.classify_image(
            "82faa041-5a9f-4dd0-b45d-fbf8d40269fc", publish_iteration_name, image_contents.read())

        # Display the results.
        for prediction in results.predictions:
            print("\t" + prediction.tag_name +
                ": {0:.2f}%".format(prediction.probability * 100))
            if prediction.tag_name == "1" or prediction.tag_name == "2" or prediction.tag_name == "3" or prediction.tag_name == "4" or prediction.tag_name == "5":
                return prediction.tag_name

def predictList(fileList): 
    predictionList = []
    for fileName in fileList:
        predictionList.append(predict(fileName))
    # print(predictionList)
    return predictionList

def listFiles():       # 1.Get file names from directory
    file_list=os.listdir("./savedFiles")
    # print (file_list)
    return file_list

def removeAll(listFiles):
    for fileName in listFiles:
        os.remove("./savedFiles/" + fileName)

def decodeImage(imageName, imgstring):
    imgdata = base64.b64decode(imgstring)
    filename = "./savedFiles/" + imageName
    with open(filename, 'wb') as f:
        f.write(imgdata)

# [name, cost, category, before, after]
def findCostDifference(assetMap, squareFootCost):
    ratio = 0
    if category == "roof":
        return {
            "name": assetMap["name"], 
            "old": 2,
            "new": 5,
            "claimAmount": 4000
        } 
    elif assetMap["category"] == "garage" or assetMap["category"] == "room" or assetMap["category"] == "basement":
         ratio = squareFootCost * assetMap["cost"]
    else:
        if assetMap["after"] == "":
            return {
                "name": assetMap["name"],
                "old": 1,
                "new": 1,
                "claimAmount": assetMap["cost"]
            }   
        else:
            return {
                "name": assetMap["name"],
                "old": 1,
                "new": 5,
                "claimAmount": assetMap["cost"]
            }  
        
    decodeImage("old.jpg", assetMap["before"])
    decodeImage("new.jpg", assetMap["after"])
    oldAmount = predict("old.jpg")
    newAmount = predict("after.jpg")
    return {
        "name": assetMap["name"],
        "old": oldAmount,
        "new": newAmount,
         "claimAmount": (int(oldAmount) - int(NewAmount)) * ratio / 5,
    }

# print(predictList(listFiles()))
# removeAll(listFiles())
# with open("damage.jpg", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())
#     decodeImage("damage.jpg", encoded_string)