import cv2
from util.Coordinate_Generator import CoordinateGenerator
from util.Car_Detector import CarDetector
from ultralytics import YOLO
from util.colors import COLOR_GREEN
from util.utils import draw_rectangles
import time


def main():
    path_to_data = "./data/coordinates.yml"
    video = cv2.VideoCapture("./parking1.mp4")
    cv2.namedWindow("parking_video")
    is_generated = False
    parking_coordinate = None
    car_detected_coordinates = None
    car_detector = CarDetector(draw_cars=True)
    for i in range((int(video.get(cv2.CAP_PROP_FRAME_COUNT)))):
        time.sleep(0.5)
        ret, frame = video.read()
        frame = cv2.resize(frame, (1020, 500))
        if ret:
            if not is_generated:
                path_to_data = "./data/coordinates.yml"
                coordinate = CoordinateGenerator(frame, path_to_data)
                coordinate.generate(is_update=False)
                parking_coordinates = coordinate.get_Coordinates()
                is_generated = True
            car_detector.detect(frame)
            car_detected_coordinates = car_detector.get_Car_Coordinates()
            for coordinate in parking_coordinates:
                draw_rectangles(
                    coordinate["coordinates"],
                    frame,
                    coordinate["is_occupied"],
                )
            cv2.imshow("parking_video", frame)
            cv2.waitKey(1)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
