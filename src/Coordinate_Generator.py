import cv2
import yaml

from util.colors import COLOR_GREEN, COLOR_BLUE
from util.utils import draw_rectangles


import cv2
import yaml

COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)


import cv2
import yaml

COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)


class CoordinateGenerator:
    """
    A class to generate coordinates for parking spaces in an image.

    ...

    Attributes
    ----------
    input_image : numpy.ndarray
        The input image to generate coordinates on.
    original_image : numpy.ndarray
        A copy of the input image.
    path_to_data : str
        The path to the file where the generated coordinates will be saved.
    is_update : bool
        A flag to indicate whether the generator is updating existing coordinates.
    preview_image : numpy.ndarray
        An image to preview the generated coordinates.
    current_point : tuple
        The current point being selected by the user.
    first_point : tuple
        The first point selected by the user to form a rectangle.
    num_points : int
        The number of points selected by the user to form a rectangle.
    id : int
        The id of the current rectangle being generated.
    current_coordinates : list
        The list of coordinates of the current rectangle being generated.
    all_coordinates : dict
        A dictionary containing all the generated coordinates.
    loaded_id : int
        The id of the last loaded rectangle from the saved coordinates file.

    Methods
    -------
    generate(is_update=False):
        Generates coordinates for parking spaces in the input image.
    __mouse_callback(event, x, y, flags, param):
        A callback function to handle mouse events.
    __handle_left_click(x, y):
        Handles left mouse button clicks.
    __handle_mouse_move(x, y):
        Handles mouse movement.
    __save_coordinates():
        Saves the generated coordinates to a file.
    __load_coordinates():
        Loads previously generated coordinates from a file.
    __erase_coordinates_in_file():
        Erases all the coordinates in the saved coordinates file.
    get_Coordinates():
        Returns a list of all the generated coordinates with their occupied status.
    """

    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, path_to_saved_coordinates):
        """
        Parameters
        ----------
        image : numpy.ndarray
            The input image to generate coordinates on.
        path_to_saved_coordinates : str
            The path to the file where the generated coordinates will be saved.
        """
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
        self.loaded_id = None

    def generate(self, is_update=False):
        """
        Generates coordinates for parking spaces in the input image.

        Parameters
        ----------
        is_update : bool, optional
            A flag to indicate whether the generator is updating existing coordinates.
            The default is False.
        """
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
                self.__erase_coordinates_in_file()
                self.original_image = self.input_image.copy()
            elif k == CoordinateGenerator.KEY_QUIT and self.num_points == 0:
                if self.id != 0:
                    self.__save_coordinates()
                break

        cv2.destroyWindow("Coordinates Generator")

    def __mouse_callback(self, event, x, y, flags, param):
        """
        A callback function to handle mouse events.

        Parameters
        ----------
        event : int
            The type of mouse event.
        x : int
            The x-coordinate of the mouse event.
        y : int
            The y-coordinate of the mouse event.
        flags : int
            The flags associated with the mouse event.
        param : object
            An optional parameter for the mouse event.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__handle_left_click(x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            self.__handle_mouse_move(x, y)

    def __handle_left_click(self, x, y):
        """
        Handles left mouse button clicks.

        Parameters
        ----------
        x : int
            The x-coordinate of the mouse click.
        y : int
            The y-coordinate of the mouse click.
        """
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
        """
        Handles mouse movement.

        Parameters
        ----------
        x : int
            The x-coordinate of the mouse.
        y : int
            The y-coordinate of the mouse.
        """
        if self.num_points > 0:
            self.preview_image = self.original_image.copy()
            cv2.line(self.preview_image, self.current_point, (x, y), COLOR_GREEN, 2)
        else:
            self.preview_image = None

    def __save_coordinates(self):
        """
        Saves the generated coordinates to a file.
        """
        mode = "a" if self.is_update else "w"

        with open(self.path_to_data, mode) as output:
            for i in self.all_coordinates:
                if mode == "a" and self.loaded_id != None and i <= self.loaded_id:
                    continue
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
        """
        Loads previously generated coordinates from a file.
        """
        with open(self.path_to_data, "r") as data:
            squares = yaml.load(data, Loader=yaml.Loader)

        if squares is None:
            return

        big_Id = 0
        for square in squares:
            points = [tuple(i) for i in square["coordinates"]]
            self.all_coordinates[square["id"]] = points
            draw_rectangles(points, self.original_image)
            if big_Id < square["id"]:
                big_Id = square["id"]
        self.loaded_id = big_Id
        self.id = big_Id + 1

    def __erase_coordinates_in_file(self):
        """
        Erases all the coordinates in the saved coordinates file.
        """
        open(self.path_to_data, "w").close()

    def get_Coordinates(self):
        """
        Returns a list of all the generated coordinates with their occupied status.

        Returns
        -------
        list
            A list of dictionaries containing the id, coordinates, and occupied status of each generated rectangle.
        """
        with_occupied_status = []
        for i in self.all_coordinates:
            with_occupied_status.append(
                {"id": i, "coordinates": self.all_coordinates[i], "is_occupied": False}
            )

        return with_occupied_status
