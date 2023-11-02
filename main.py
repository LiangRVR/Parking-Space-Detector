import cv2
from util.Coordinate_Generator import CoordinateGenerator


def main():
    img = cv2.imread("./parking_lot_1.png")
    path_to_data = "./data/coordinates.yml"
    coordinate = CoordinateGenerator(img, path_to_data,is_update=True)
    coordinate.generate()


if __name__ == '__main__':
    main()
