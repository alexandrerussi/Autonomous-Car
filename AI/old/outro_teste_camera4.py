import numpy as np
import cv2
import scipy.ndimage as ndi

#img = cv2.imread(path)

video = cv2.VideoCapture(1)
while(video.isOpened()):
    ret, orig_frame = video.read()
    gray = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2GRAY)  
    smooth = ndi.filters.median_filter(gray, size=2)
    edges = smooth > 180  
    lines = cv2.HoughLinesP(edges.astype(np.uint8), 0.5, np.pi/180, 120)

    for rho,theta in lines[0]:
        print(rho, theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(orig_frame,(x1,y1),(x2,y2),(0,0,255),2)

    # Show the result
    cv2.imshow("Line Detection", orig_frame)
    cv2.imshow("gray", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()