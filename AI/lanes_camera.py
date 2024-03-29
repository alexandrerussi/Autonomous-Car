import cv2 # importanto opencv
import numpy as np


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

def canny(image): # transforma a img de rgb para cinza
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

def region_of_interest(image): # corta img para regiao de interesse
    height = image.shape[0]
    polygons = np.array([
        #[(200, height), (1100, height), (550, 250)]
        [(50, height), (600, height), (275, 0)] # forma um triangulo
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

cap = cv2.VideoCapture(0) # captura do video webcam
while(cap.isOpened()): # loop de tempo indeterinado, enquanto a camera estiver aberto
    _, frame = cap.read() # leitura da camera, as imagens em si
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)

    #agrupar todos os parametros de linha solicitados e guarda no array lines
    # lines tera a coordenada total da linha
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5) 
    #print(lines)

    left = 0
    right = 0
    if not lines is None: # verificar se existe linha na esquerda e na direita
        for line in list(lines):
            print(list(lines))
            print(line[0])
            if line[0][0] > 0 and line[0][0] < 270 and line[0][1] >= 0 and line[0][1] < 200 and (line[0][0]-line[0][2]) < 100:
                left = 1

            if line[0][0] > 310 and line[0][0] < 640 and line[0][1] >= 0 and line[0][1] < 200 and (line[0][0]-line[0][2]) < 100:
                right = 1

        if left and right:
            print("TUDO CERTO")
        elif left and not right:
            print("VIRA DIREITA")
        else:
            print("VIRA ESQUERDA")
    
    # retangulo que aparece na primeira imagem
    point1, point2, point3, point4 = (50, 0), (600, 0), (0, 475), (640,475)
    img = cv2.line(frame, point1, point2, (0,0,255), 2)
    img = cv2.line(frame, point2, point4, (0,0,255), 2)
    img = cv2.line(frame, point4, point3, (0,0,255), 2)
    img = cv2.line(frame, point3, point1, (0,0,255), 2)
    #lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=80)
    #averaged_lines = average_slope_intercept(frame, lines)
    #line_image = display_lines(frame, averaged_lines)
    #combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow("result", cropped_image) # mostra a camera na tela
    cv2.imshow("frame", frame) # mostra a camera sem filtro nenhum
    if cv2.waitKey(1) & 0xFF == ord('q'): # aperta q fecha camera
        break
cap.release() # ficar executar camera
cv2.destroyAllWindows() # fecha tudo que tinha antes