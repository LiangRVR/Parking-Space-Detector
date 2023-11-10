import cv2
from shapely.geometry import Point, Polygon
from util.Coordinate_Generator import CoordinateGenerator
from util.Car_Detector import CarDetector
from util.utils import draw_rectangles
import time


class ParkingSpaceDetector:
    KEY_QUIT = ord("q")

    def __init__(self, video_path, path_to_coordinate_data, draw_cars=True):
        self.video_path = video_path
        self.path_to_data = path_to_coordinate_data
        self.is_generated = False
        self.parking_coordinates = None
        self.car_detected_coordinates = None
        self.car_detector = CarDetector(draw_cars=draw_cars)

    def check_parking_spot_occupied(self):
        video = cv2.VideoCapture(self.video_path)
        cv2.namedWindow("parking_video")
        for i in range((int(video.get(cv2.CAP_PROP_FRAME_COUNT)))):
            time.sleep(0.3)
            ret, frame = video.read()
            frame = cv2.resize(frame, (1020, 500))
            if ret:
                self.generate_parking_coordinates(frame)

                self.detect_cars(frame)

                if self.car_detected_coordinates is not None:
                    self.set_parking_spots_occupied()
                    self.draw_parking_spots(frame)
                    
                cv2.imshow("parking_video", frame)
            k = cv2.waitKey(1) & 0xFF

            if k == CoordinateGenerator.KEY_QUIT:
                break
        cv2.destroyAllWindows()

    def generate_parking_coordinates(self, frame):
        if not self.is_generated:
            coordinate = CoordinateGenerator(frame, self.path_to_data)
            coordinate.generate(is_update=True)
            self.parking_coordinates = coordinate.get_Coordinates()
            self.is_generated = True

    def detect_cars(self, frame):
        self.car_detector.detect(frame)
        self.car_detected_coordinates = self.car_detector.get_Car_Coordinates()

    def set_parking_spots_occupied(self):
        for i in range(len(self.parking_coordinates)):
            for car in self.car_detected_coordinates:
                cx = car["low_center"][0]
                cy = car["low_center"][1]
                polygon = Polygon(self.parking_coordinates[i]["coordinates"])
                point = Point(cx, cy)
                is_occupied = polygon.contains(point)
                self.parking_coordinates[i]["is_occupied"] = is_occupied
                if is_occupied:
                    break

    def draw_parking_spots(self, frame):
        for coordinate in self.parking_coordinates:
            draw_rectangles(
                coordinate["coordinates"],
                frame,
                is_occupied=coordinate["is_occupied"],
            )
