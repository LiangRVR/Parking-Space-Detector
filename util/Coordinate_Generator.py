import cv2
import yaml

from util.colors import COLOR_GREEN, COLOR_BLUE


class CoordinateGenerator:
    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, path_to_saved_coordinates, is_update=False):
        self.input_image = image
        self.original_image = image.copy()
        self.path_to_data = path_to_saved_coordinates
        self.is_update = is_update

        self.preview_image = None
        self.current_point = (-1, -1)
        self.first_point = (-1, -1)
        self.num_points = 0
        self.id = 0
        self.current_coordinates = []
        self.all_coordinates = {}

    def generate(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.__mouse_callback)
        if self.is_update:
            self.__load_coordinates()

        while True:
            if self.preview_image is None:
                cv2.imshow("image", self.original_image)
            else:
                cv2.imshow("image", self.preview_image)

            k = cv2.waitKey(1) & 0xFF

            if k == CoordinateGenerator.KEY_RESET:
                self.id = 0
                self.current_coordinates = []
                self.all_coordinates = {}
                self.preview_image = None
                self.num_points = 0
                self.original_image = self.input_image.copy()
            elif k == CoordinateGenerator.KEY_QUIT and self.num_points == 0:
                if self.id != 0:
                    self.__save_coordinates()
                break

        cv2.destroyAllWindows()

    def __mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__handle_left_click(x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            self.__handle_mouse_move(x, y)

    def __handle_left_click(self, x, y):
        if self.num_points == 0:
            self.first_point = (x, y)

        if self.num_points != 0:
            cv2.line(self.original_image, self.current_point, (x, y), COLOR_BLUE, 1)

        self.current_point = (x, y)
        self.current_coordinates.append(self.current_point)
        self.num_points += 1

        if self.num_points == 4:
            self.all_coordinates[self.id] = self.current_coordinates
            self.id += 1
            self.num_points = 0
            self.current_coordinates = []
            cv2.line(
                self.original_image, self.current_point, self.first_point, COLOR_BLUE, 1
            )

    def __handle_mouse_move(self, x, y):
        if self.num_points > 0:
            self.preview_image = self.original_image.copy()
            cv2.line(self.preview_image, self.current_point, (x, y), COLOR_GREEN, 1)
        else:
            self.preview_image = None

    def __save_coordinates(self):
        print(self.all_coordinates)
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
            output.close()

    def __load_coordinates(self):
        with open(self.path_to_data, "r") as data:
            squares = yaml.load(data, Loader=yaml.Loader)

        big_Id = 0
        for square in squares:
            points = square["coordinates"]
            self.__draw_points(points)
            if big_Id < square["id"]:
                big_Id = square["id"]
        self.id = big_Id + 1
        data.close()

    def __draw_points(self, points):
        point_1 = points[0]
        for i in range(1, len(points)):
            cv2.line(self.original_image, tuple(point_1), tuple(points[i]), COLOR_BLUE, 1)
            point_1 = points[i]
