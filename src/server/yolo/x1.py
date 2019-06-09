import os
from darknet import performDetect

# Wrapper for performDetect using yolo-tiny
def getResult(path="LinkLaser/1.jpg"):
    result = performDetect(imagePath = path, configPath = "./yolo-link.cfg",
                           weightPath = "./yolo-link_final.weights",
                           metaPath = "./link.data",
                           showImage = False,
                           makeImageOnly = False, initOnly = False)
    return result

imglist = [file for file in os.listdir('LinkLaser') if file.endswith('.jpg')]

print(imglist)
print("{} images found".format(len(imglist)))


for img in imglist:
    print("Predicting LinkLaser/"+img)
    result = getResult("LinkLaser/"+img)
    print(result)
