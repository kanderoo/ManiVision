import VisionTables
import cv2
import csv
import numpy as np


def nothing(x):
    pass


cap = cv2.VideoCapture(0)
cv2.namedWindow('sliders')
cv2.createTrackbar('hL', 'sliders', 0, 255, nothing)
cv2.createTrackbar('sL', 'sliders', 0, 255, nothing)
cv2.createTrackbar('vL', 'sliders', 0, 255, nothing)
cv2.createTrackbar('hU', 'sliders', 0, 255, nothing)
cv2.createTrackbar('sU', 'sliders', 0, 255, nothing)
cv2.createTrackbar('vU', 'sliders', 0, 255, nothing)
cv2.createTrackbar('dilation', 'sliders', 0, 50, nothing)
cv2.createTrackbar('erosion', 'sliders', 0, 50, nothing)
cv2.createTrackbar('writeToFile', 'sliders', 0, 1, nothing)
cv2.createTrackbar('readFromFile', 'sliders', 0, 1, nothing)

# Setup NetworkTables
while 1:
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([255, 255, 255])
    cv2.imshow('sliders', frame)
    # get current positions of four trackbars
    lower_blue[(0)] = cv2.getTrackbarPos('hL', 'sliders')
    lower_blue[(1)] = cv2.getTrackbarPos('sL', 'sliders')
    lower_blue[(2)] = cv2.getTrackbarPos('vL', 'sliders')
    upper_blue[(0)] = cv2.getTrackbarPos('hU', 'sliders')
    upper_blue[(1)] = cv2.getTrackbarPos('sU', 'sliders')
    upper_blue[(2)] = cv2.getTrackbarPos('vU', 'sliders')
    erodeAmount = cv2.getTrackbarPos('erosion', 'sliders')
    dilateAmount = cv2.getTrackbarPos('dilation', 'sliders')
    writeToFile = cv2.getTrackbarPos('writeToFile', 'sliders')
    readFromFile = cv2.getTrackbarPos('readFromFile', 'sliders')
    # If write to file is equal to one, then write values to CSV file.
    if writeToFile == 1:
        with open('HSV_Values.csv', mode='w') as HSV_Values:
            employee_writer = csv.writer(HSV_Values, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(
                ['Lower Hue ', 'Lower Saturation', 'Lower Value', 'Upper Hue', 'Upper Saturation', 'Upper Value',
                 'Dilation', 'Erosion'])
            employee_writer.writerow(
                [str(lower_blue[(0)]), str(lower_blue[(1)]), str(lower_blue[(2)]), str(upper_blue[(0)]),
                 str(upper_blue[(1)]), str(upper_blue[(2)]), str(dilateAmount), str(erodeAmount)])

    # Threshold the HSV image to
    if readFromFile == 1:
        with open('HSV_Values.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    lower_blue[(0)] = int(row[0])
                    lower_blue[(1)] = int(row[1])
                    lower_blue[(2)] = int(row[2])
                    upper_blue[(0)] = int(row[3])
                    upper_blue[(1)] = int(row[4])
                    upper_blue[(2)] = int(row[5])
                    dilateAmount = int(row[6])
                    erodeAmount = int(row[7])
                    line_count += 1
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    erosion = cv2.erode(mask, kernel, iterations=erodeAmount)
    dilation = cv2.dilate(erosion, kernel, iterations=dilateAmount)
    # Bitwise-AND mask and original image
    img2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, [contours[0]], 0, (255, 0, 255), 3)
    try:
        x, y, w, h = cv2.boundingRect(contours[0])
        centerX = x + (w / 2)
        centerY = y + (h / 2)
        # cv2.putText(frame, centerX, org, FONT_HERSHEY_SIMPLEX, (255, 0, 255));
        VisionTables.sendX(centerX)
        VisionTables.sendY(centerY)
    except:
        print("Exception: You're probably an idiot (Formerly: Mani is doodoo")
    cv2.imshow('mask', dilation)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
