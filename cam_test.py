# program to capture single image from webcam in python 

# importing OpenCV library 
import cv2 as cv

def faceRecognition(image):
    front_faces_list = []
    # Load the cascade
    face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    front_faces_list.append(face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40)))

    profile_faces_list = []
    face_cascade = cv.CascadeClassifier('haarcascade_profileface.xml')
    profile_faces_list.append(face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(40, 40)))

    # Search for close centroids
    for front_faces in front_faces_list:
        for profile_faces in profile_faces_list:
            for (x1, y1, w1, h1) in front_faces:
                for (x2, y2, w2, h2) in profile_faces:
                    if abs(x1 - x2) < 100 and abs(y1 - y2) < 100:
                        max_height = max(h1, h2)
                        max_width = max(w1, w2)
                        min_x = min(x1, x2)
                        min_y = min(y1, y2)
                        cv.rectangle(image, (min_x, min_y), (min_x + max_width, min_y + max_height), (0, 255, 255), 2)
                        front_faces_list.remove(front_faces)
                        profile_faces_list.remove(profile_faces)
                        break

    # Detect faces
    # Draw rectangle around the faces
    for faces in profile_faces_list:
        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    for faces in front_faces_list:
        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# initialize the camera 
# If you have multiple camera connected with 
# current device, assign a value in cam_port 
# variable according to that 
cam_port = 0
cam = cv.VideoCapture(cam_port) 

# reading the input using the camera 
result, image = cam.read() 

# If image will detected without any error, 
# show result 
while result: 

    faceRecognition(image)

	# showing result, it take frame name and image 
	# output 
    cv.imshow("FaceDetector", image) 

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    result, image = cam.read() 

cam.release()
cv.destroyAllWindows()
