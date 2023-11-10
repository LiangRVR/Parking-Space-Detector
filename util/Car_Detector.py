import cv2
from ultralytics import YOLO
from util.colors import COLOR_WHITE


class CarDetector:
    def __init__(self, draw_cars= False):
        self.model = YOLO("yolov8x.pt")
        self.draw_cars = draw_cars
        self.class_id = [2, 3, 5, 7]
        self.input_image = None

    def detect(self, image):
        self.input_image = image
        self.cars_detected = []
        prediction = self.model.predict(
            self.input_image, classes=self.class_id, device=0, verbose=False
        )
        for result in prediction:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                box_coordinates = box.xyxy[0].astype(int)
                down_the_center = (box_coordinates[1] + 7 * box_coordinates[3]) / 8
                low_center = (
                    int((box_coordinates[0] + box_coordinates[2]) / 2),
                    int(down_the_center),
                )
                card_detected = {
                    "x_1": box_coordinates[0],
                    "y_1": box_coordinates[1],
                    "x_2": box_coordinates[2],
                    "y_2": box_coordinates[3],
                    "low_center": low_center,
                }
                self.cars_detected.append(card_detected)
                if self.draw_cars:
                    self.draw_car_detected(card_detected)

    def get_Car_Coordinates(self):
        return self.cars_detected

    def draw_car_detected(self, car):
        cv2.rectangle(
            self.input_image,
            (car["x_1"], car["y_1"]),
            (car["x_2"], car["y_2"]),
            COLOR_WHITE,
            1,
        )
        cv2.circle(self.input_image, car["low_center"], 1, COLOR_WHITE, 1)
