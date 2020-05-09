import os
import searchImage
import mouseHandle

# Find Images area
picturesDic = {}
with os.scandir('testpictures/') as files:
    for file in files:
        print(file.path)
        print(file.name)
        picturesDic.update({file.name:file.path})


print(picturesDic)

for names in picturesDic:
    print(names)
    print(picturesDic[names])

resultArray = []

numImages = 0
nameFiles = ""

for pictureNames in picturesDic:
    # Check for each photo
    print("We're looking for: {}".format(pictureNames))
    resultArray = searchImage.imageSearch(picturesDic[pictureNames])
    # print Results
    print(resultArray)
    # if it found the photo then click location
    if resultArray[0] is 'true':
        print("image Found")
        mouseHandle.clickPlace(resultArray[1], resultArray[2])
        numImages +=1
        nameFiles = nameFiles + pictureNames + " "
    else:
        print("image not found nothing to do")

print("Number of images Found: {}".format(numImages))
print("Names of the Files image Found \n {}".format(nameFiles))