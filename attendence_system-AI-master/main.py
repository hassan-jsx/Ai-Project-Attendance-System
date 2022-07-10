# Libraries/dependies use for project. As we install packages
# like: dlib, open-cv, face-recognition, cmake and others

import face_recognition
import cv2
import numpy as np

# We use two images for each person. 1st is for training and other is for testing.
# Training image is to get encodings of the image to be identifiy later to make attendence system.
imgIK = face_recognition.load_image_file('images/IK-training.jpg')
# as our image are in BGR and library understands RGB.
imgIK = cv2.cvtColor(imgIK,cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('images/IK-Test.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)

# Now we will find the encoding of image for training
# for this we have to do detect the face in image, in result we get top,right,bottom and left of image
# after detection we do encode the face
faceLoc_train = face_recognition.face_locations(imgIK)[0]
encode_training = face_recognition.face_encodings(imgIK)[0]
cv2.rectangle(imgIK,(faceLoc_train[3],faceLoc_train[0]),(faceLoc_train[1],faceLoc_train[2]),(255,0,255),2)
# top, right, bottom, left , color, thickness of rectangle

faceLoc_test = face_recognition.face_locations(imgTest)[0]
encode_testing = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLoc_test[3],faceLoc_test[0]),(faceLoc_test[1],faceLoc_test[2]),(255,0,255),2)
# top, right, bottom, left , color, thickness of rectangle

# We now have encoding of both training and testing image. To make attendence system we have to compare both encodings
# for comparison we use 128 measurements return by encodings and we use ML algorithm SVM classifier for matching encodings
results = face_recognition.compare_faces([encode_training], encode_testing)
# compare_faces return true/false on matching encodings
faceDis = face_recognition.face_distance([encode_training], encode_testing)
# we are using distance to do best match. Becuase once we will have a lot of images we can find similarities.
# Lower distance shows better match and vice versa
cv2.putText(imgTest,f'{results} {round(faceDis[0],2)} ',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)

cv2.imshow('IK-Train' , imgIK)
cv2.imshow('IK-Test' , imgTest)
cv2.waitKey(0)

