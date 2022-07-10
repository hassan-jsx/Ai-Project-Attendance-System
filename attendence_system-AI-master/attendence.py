from datetime import datetime

import face_recognition
import cv2
import numpy as np
import os

# now the get the data for persons like: students of BSCS-VI to make there attendence.
path = 'persons_data'
images = []
className = []
myList = os.listdir(path)

for x,cl in enumerate(myList):
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    className.append(os.path.splitext(cl)[0])

# Now we will do the encodings of each image.
def findEncodings(images):
    # to save encodings of images data
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    # with readung and writing at the same time
    # similarly we make sure that one who arrieved then it wont mark again
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList =[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in  line:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            f.writelines(f'n{name},{dt_string}')

encodeTest = findEncodings(images)

# initializing web cam for taking attendence
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    # reducing size of images on real time to make system processing fast
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Here we are finding location and encodings of current frame from runtime webcam frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    # matching encodetest and encodeface to check attendence and match it from our database images
    # zip is used to make both encodesCurFrame and facesCurFrame in the same loop
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeTest, encodeFace)
        faceDis = face_recognition.face_distance(encodeTest, encodeFace)
        print(faceDis)
        # now we find the minimum one, as this would be the best match.
        matchIndex = np.argmin(faceDis)

        # if matches[matchIndex]:
        #     name = className[matchIndex].upper()
        #     # print(name)
        #     y1, x2, y2, x1 = faceLoc
        #     # as we scalled images to 0.25 (one forth), so here for good location detecting1 we multiply it by four
        #     y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        #     cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        #     cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        #     markAttendance(name)

        if faceDis[matchIndex] < 0.50:
            name = className[matchIndex].upper()
            markAttendance(name)
        else:
            name = 'Unknown'
        # print(name)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

# print(len(encodeTest)) checking the encoded list
# print(myList)
# print("Total Classes Detected:",len(myList))
# print(className)

# We use two images for each person. 1st is for training and other is for testing.
# Training image is to get encodings of the image to be identifiy later to make attendence system.
# imgIK = face_recognition.load_image_file('images/IK-training.jpg')
# as our image are in BGR and library understands RGB.
# imgIK = cv2.cvtColor(imgIK,cv2.COLOR_BGR2RGB)
# imgTest = face_recognition.load_image_file('images/IK-Test.jpg')
# imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

