import cv2
import numpy as np

#Point2f Source[] = {Point2f(50,200), Point2f(200,200),Point2f(0,240),Point2f(360,240)}
Source = np.float32([[50, 200], [600, 200], [0, 475], [640,475]])
Destination = np.float32([[60, 0], [300, 0], [60, 475], [300,475] ])

point1, point2, point3, point4 = (50, 200), (600, 200), (0, 475), (640,475)
dest_point1, dest_point2, dest_point3, dest_point4 = (60, 0), (300, 0), (60, 240), (300,240) 

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

cap = cv2.VideoCapture(1)
while(cap.isOpened()):
    _, frame = cap.read()
    _, frame1 = cap.read()
    
    img = cv2.line(frame, point1, point2, (0,0,255), 2)
    img = cv2.line(frame, point2, point4, (0,0,255), 2)
    img = cv2.line(frame, point4, point3, (0,0,255), 2)
    img = cv2.line(frame, point3, point1, (0,0,255), 2)

    matrix = cv2.getPerspectiveTransform(Source, Destination)
    warp = cv2.warpPerspective(frame, matrix, (600, 475))
    gray = cv2.cvtColor(warp, cv2.COLOR_RGB2GRAY)
    gray1 = cv2.inRange(gray, 240, 255)
    gray2 = cv2.Canny(gray, 100, 500)

    #dst = cv2.addWeighted(gray1,0.7,gray2,0.3,0)
    dst = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    vector = []
    vector_2 = np.array([])

    for i in range(len(dst)):
        #print (i)
        #ROILane = cv2.rectangle(dst, (i, 140), (1, 100), (0,0,255))
        #t = cv2.divide(255, ROILane, ROILane)
        #print(sum(dst[i,140]))
        #np.append(vector, sum(dst[i,140]))
        vector.append(sum(dst[i,140]))
        vector_2 = np.append(vector_2, sum(dst[i,140]))

    
    leftPtr = max(vector[0], vector[220])
    result = np.where(vector_2 == np.amax(vector_2))[0]
    print(result[0])

    dst = cv2.line(dst, (result[0], 0), (result[0], 240), (0,0,255), 2)

    rightPtr = max(vector[221], vector[474])
    result1 = np.where(vector_2 == np.amax(vector_2))[0]

    dst = cv2.line(dst, (result1[0], 0), (result1[0], 240), (0,0,255), 2)

    dst = cv2.line(dst, (225, 0), (225, 475), (0,255,0), 2)

    #leftPtr = np.array([])
    #leftPtr = max(vector[0], vector[150])

    #lines = cv2.HoughLinesP(dst, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

    cv2.imshow("Original", img) 
    #cv2.imshow("Perspective", warp)
    cv2.imshow("Gray", dst)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()