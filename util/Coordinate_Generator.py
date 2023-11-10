import cv2
import yaml

from util.colors import COLOR_GREEN, COLOR_BLUE
from util.utils import draw_rectangles


class CoordinateGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, path_to_saved_coordinates):
        self.input_image = image
        self.original_image = image.copy()
        self.path_to_data = path_to_saved_coordinates

        self.is_update = False
        self.preview_image = None
        self.current_point = (-1, -1)
        self.first_point = (-1, -1)
        self.num_points = 0
        self.id = 0
        self.current_coordinates = []
        self.all_coordinates = {}

    def generate(self, is_update=False):
        self.is_update = is_update
        cv2.namedWindow("Coordinates Generator")
        cv2.setMouseCallback("Coordinates Generator", self.__mouse_callback)
        if self.is_update:
            self.__load_coordinates()

        while True:
            if self.preview_image is None:
                cv2.imshow("Coordinates Generator", self.original_image)
            else:
                cv2.imshow("Coordinates Generator", self.preview_image)

            k = cv2.waitKey(1) & 0xFF

            if k == CoordinateGenerator.KEY_RESET:
                self.id = 0
                self.current_coordinates = []
                self.all_coordinates = {}
                self.preview_image = None
                self.num_points = 0
                self.is_update = False
                self.original_image = self.input_image.copy()
            elif k == CoordinateGenerator.KEY_QUIT and self.num_points == 0:
                if self.id != 0:
                    self.__save_coordinates()
                break

        cv2.destroyWindow("Coordinates Generator")

    def __mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__handle_left_click(x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            self.__handle_mouse_move(x, y)

    def __handle_left_click(self, x, y):
        if self.num_points == 0:
            self.first_point = (x, y)

        if self.num_points != 0:
            cv2.line(self.original_image, self.current_point, (x, y), COLOR_BLUE, 2)

        self.current_point = (x, y)
        self.current_coordinates.append(self.current_point)
        self.num_points += 1

        if self.num_points == 4:
            self.all_coordinates[self.id] = self.current_coordinates
            self.id += 1
            self.num_points = 0
            self.current_coordinates = []
            cv2.line(
                self.original_image, self.current_point, self.first_point, COLOR_BLUE, 2
            )

    def __handle_mouse_move(self, x, y):
        if self.num_points > 0:
            self.preview_image = self.original_image.copy()
            cv2.line(self.preview_image, self.current_point, (x, y), COLOR_GREEN, 2)
        else:
            self.preview_image = None

    def __save_coordinates(self):
        mode = "a" if self.is_update else "w"

        with open(self.path_to_data, mode) as output:
            for i in self.all_coordinates:
                output.write(
                    "-\n          id: "
                    + str(i)
                    + "\n          coordinates: ["
                    + "["
                    + str(self.all_coordinates[i][0][0])
                    + ","
                    + str(self.all_coordinates[i][0][1])
                    + "],"
                    + "["
                    + str(self.all_coordinates[i][1][0])
                    + ","
                    + str(self.all_coordinates[i][1][1])
                    + "],"
                    + "["
                    + str(self.all_coordinates[i][2][0])
                    + ","
                    + str(self.all_coordinates[i][2][1])
                    + "],"
                    + "["
                    + str(self.all_coordinates[i][3][0])
                    + ","
                    + str(self.all_coordinates[i][3][1])
                    + "]]\n"
                )

    def __load_coordinates(self):
        with open(self.path_to_data, "r") as data:
            squares = yaml.load(data, Loader=yaml.Loader)

        big_Id = 0
        for square in squares:
            points = [tuple(i) for i in square["coordinates"]]
            self.all_coordinates[square["id"]] = points
            draw_rectangles(points, self.original_image)
            if big_Id < square["id"]:
                big_Id = square["id"]
        self.id = big_Id + 1



    def get_Coordinates(self):
        with_occupied_status = []
        for i in self.all_coordinates:
            with_occupied_status.append(
                {"id": i, "coordinates": self.all_coordinates[i], "is_occupied": False}
            )

        return with_occupied_status
