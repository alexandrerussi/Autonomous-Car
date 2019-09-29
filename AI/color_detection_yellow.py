#importing Modules
import cv2
import numpy as np

def detect(img):
    cascade = cv2.CascadeClassifier("cascade.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, 0, (20,20))
    #print(rects)
    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img


def make_int(number):
    if number % 2 != 0:
        number = number - 1
    return int(number)


def smallest_box(raw_squares):
    index_smallest_square = 0
    if len(raw_squares) > 1:
        # Assumes you'll only ever see one set of concentric squares, which won't
        # always be true. Would need to test for different square centers
        i = 0
        for x1, y1, x2, y2 in raw_squares:
            x1s = raw_squares[index_smallest_square][0]
            y1s = raw_squares[index_smallest_square][1]
            x2s = raw_squares[index_smallest_square][2]
            y2s = raw_squares[index_smallest_square][3]
            if x1 > x2s and y1 < y1s and x2 < x2s and y2 < y2s:
                index_smallest_square = i
    return index_smallest_square


def box(rects, img):
    index_smallest_square = smallest_box(rects)
    i = 0
    for x1, y1, x2, y2 in rects:
        y_diff = make_int(y1 - y2)
        x_average = make_int((x1 + x2) / 2)
        new_x1 = x_average - make_int((y_diff / 2))
        new_x2 = x_average + make_int((y_diff / 2))
        if i == index_smallest_square:
            # last arguement is the thickness of the bounding box
            cv2.rectangle(img, (new_x1, y1), (new_x2, y2), (127, 255, 0), 2)
        i = i + 1

def detect_stop_sign(frame):
    rects, img = detect(frame)
    box(rects, frame)
    #cv2.imshow("frame", frame)
    return frame

#Capturing Video through webcam.
cap = cv2.VideoCapture(1)
while True:
    _, img = cap.read()
    '''rects, img = detect(img)
    box(rects, img)
    cv2.imshow("frame", img)
    if len(rects):
        print("List is empty")
    else:
        print("Nothing")'''

    #converting frame(img) from BGR (Blue-Green-Red) to HSV (hue-saturation-value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #defining the range of Yellow color
    #yellow_lower = np.array([22,60,200],np.uint8)
    #yellow_upper = np.array([60,255,255],np.uint8)

    #green_lower = np.array([22,60,200], np.uint8)
    # green_lower = np.array([110,50,50], np.uint8)
    # green_upper = np.array([130,255,255], np.uint8)

    green_lower = np.array([0,200,190], np.uint8)
    green_upper = np.array([130,255,0], np.uint8)

    lower_red = np.array([0,176,240]) 
    upper_red = np.array([130,255,255])

    blue_lower = np.array([0, 176, 240], np.uint8)
    blue_upper = np.array([102, 255, 255], np.uint8)

    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])

    #finding the range yellow colour in the image
    yellow = cv2.inRange(hsv, green_lower, green_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)

    #Morphological transformation, Dilation        
    kernal = np.ones((5 ,5), "uint8")
    blue=cv2.dilate(yellow, kernal)
    res=cv2.bitwise_and(img, img, mask = yellow)

    '''blue2=cv2.dilate(blue, kernal)
    res=cv2.bitwise_and(img, img, mask = blue2)'''

    #Tracking Colour (Yellow) 
    contours, hierarchy = cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    print("PROCURADNO")
            
    for pic, contour in enumerate(contours):
        print("entrou no for")
        area = cv2.contourArea(contour)
        print(area)
        if(area>300):
            print("ACHOU VERDE")
            x,y,w,h = cv2.boundingRect(contour)     
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
    
    '''contours, hierarchy = cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour)     
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
            print("ACHOU AZUL")'''
    

    #Display results
    img = cv2.flip(img,1)
    cv2.imshow("Yellow",res)

    cv2.imshow("Color Tracking",img)
    if cv2.waitKey(10) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break