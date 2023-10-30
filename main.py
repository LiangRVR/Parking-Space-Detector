import cv2
from util.Coordinate_Generator import CoordinateGenerator

def main():
    img = cv2.imread("./parking_lot_1.png")
    coordinate = CoordinateGenerator(img, "./coordinates.txt")
    coordinate.generate()

main()
