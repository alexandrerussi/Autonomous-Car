import cv2
import numpy as np

Source = np.float32([[50, 200], [600, 200], [0, 475], [640,475]])
Destination = np.float32([[60, 0], [300, 0], [60, 475], [300,475] ])

point1, point2, point3, point4 = (50, 200), (600, 200), (0, 475), (640,475)
dest_point1, dest_point2, dest_point3, dest_point4 = (60, 0), (300, 0), (60, 240), (300,240) 

cap = cv2.VideoCapture(1)
while(cap.isOpened()):
    _, frame = cap.read()
    
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

    for i in range(len(gray)):
        #print(gray[i, 100])
        ola = cv2.rectangle(gray, (i, 140), (1, 100), (0,0,255))
        vector.append(ola[i,100])
        vector_2 = np.append(vector_2, ola[i,100])

    part1 = vector_2[0:170]
    part2 = vector_2[190:475]
    result = np.where(part1 > 240)[0]
    result2 = np.where(part2 > 240)[0]
    
    dst = cv2.line(gray, (180, 0), (180, 500), (255,0,0), 2)

    if len(result) > 0 and len(result2) > 0:
        dst = cv2.line(gray, (result[0], 0), (result[0], 500), (0,255,255), 2)
        dst = cv2.line(gray, (result2[0], 0), (result2[0], 500), (0,255,255), 2)

    cv2.imshow("Original", img) 
    #cv2.imshow("Perspective", warp)
    cv2.imshow("Gray", dst)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()