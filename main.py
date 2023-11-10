import cv2
from shapely.geometry import Point, Polygon
from util.Coordinate_Generator import CoordinateGenerator
from util.Car_Detector import CarDetector
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
        time.sleep(0.3)
        ret, frame = video.read()
        frame = cv2.resize(frame, (1020, 500))
        if ret:
            if not is_generated:
                path_to_data = "./data/coordinates.yml"
                coordinate = CoordinateGenerator(frame, path_to_data)
                coordinate.generate(is_update=True)
                parking_coordinates = coordinate.get_Coordinates()
                is_generated = True
            car_detector.detect(frame)
            car_detected_coordinates = car_detector.get_Car_Coordinates()
            if car_detected_coordinates is not None:
                for i in range(len(parking_coordinates)):
                    for car in car_detected_coordinates:
                        cx = car["low_center"][0]
                        cy = car["low_center"][1]
                        polygon = Polygon(parking_coordinates[i]["coordinates"])
                        point = Point(cx, cy)
                        is_occupied = polygon.contains(point)
                        if is_occupied:
                            parking_coordinates[i]["is_occupied"] = True
                            break
                        else:
                            parking_coordinates[i]["is_occupied"] = False

                for coordinate in parking_coordinates:
                    draw_rectangles(
                        coordinate["coordinates"],
                        frame,
                        is_occupied=coordinate["is_occupied"],
                    )
            cv2.imshow("parking_video", frame)
            cv2.waitKey(1)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
