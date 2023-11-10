import cv2
from ultralytics import YOLO
from util.colors import COLOR_WHITE


class CarDetector:
    """
    A class used to detect cars in an image using YOLOv8x object detection model.

    Attributes
    ----------
    model : YOLO
        The YOLOv8x object detection model used for car detection.
    draw_cars : bool
        A flag indicating whether to draw the detected cars on the input image.
    class_id : list
        A list of class IDs for car detection.
    input_image : numpy.ndarray
        The input image for car detection.
    cars_detected : list
        A list of dictionaries containing the coordinates of the detected cars.

    Methods
    -------
    detect(image)
        Detects cars in the input image and stores their coordinates in the cars_detected attribute.
    get_Car_Coordinates()
        Returns the list of dictionaries containing the coordinates of the detected cars.
    draw_car_detected(car)
        Draws the detected car on the input image.
    """

    def __init__(self, draw_cars= False):
        self.model = YOLO("yolov8x.pt")
        self.draw_cars = draw_cars
        self.class_id = [2, 3, 5, 7]
        self.input_image = None
        self.cars_detected = []

    def detect(self, image):
        """
        Detects cars in the input image and stores their coordinates in the cars_detected attribute.

        Parameters
        ----------
        image : numpy.ndarray
            The input image for car detection.
        """
        self.input_image = image
        self.cars_detected = []
        prediction = self.model.predict(
            self.input_image, classes=self.class_id, device=0, verbose=False
        )
        for result in prediction:
            boxes = result.boxes.cpu().numpy()
            for box in boxes:
                box_coordinates = box.xyxy[0].astype(int)
                down_the_center = (box_coordinates[1] + 3 * box_coordinates[3]) / 4
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
        """
        Returns the list of dictionaries containing the coordinates of the detected cars.

        Returns
        -------
        list
            A list of dictionaries containing the coordinates of the detected cars.
        """
        return self.cars_detected

    def draw_car_detected(self, car):
        """
        Draws the detected car on the input image.

        Parameters
        ----------
        car : dict
            A dictionary containing the coordinates of the detected car.
        """
        cv2.rectangle(
            self.input_image,
            (car["x_1"], car["y_1"]),
            (car["x_2"], car["y_2"]),
            COLOR_WHITE,
            1,
        )
        cv2.circle(self.input_image, car["low_center"], 1, COLOR_WHITE, 1)
