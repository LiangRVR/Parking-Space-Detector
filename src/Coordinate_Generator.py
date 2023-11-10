import cv2
import yaml

from util.colors import COLOR_GREEN, COLOR_BLUE
from util.utils import draw_rectangles


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
    KEY_RESET : int
        The ASCII code for the 'r' key, used to reset the generator.
    KEY_QUIT : int
        The ASCII code for the 'q' key, used to quit the generator.
    input_image : numpy.ndarray
        The input image to generate coordinates for.
    original_image : numpy.ndarray
        A copy of the input image.
    path_to_data : str
        The path to the file where the generated coordinates will be saved.
    is_update : bool
        A flag indicating whether the generator is being used to update existing coordinates.
    preview_image : numpy.ndarray
        An image with a preview of the current coordinates being generated.
    current_point : tuple
        The current point being selected by the user.
    first_point : tuple
        The first point selected by the user to define a parking space.
    num_points : int
        The number of points selected so far to define a parking space.
    id : int
        The ID of the current parking space being defined.
    current_coordinates : list
        A list of the current coordinates being defined for a parking space.
    all_coordinates : dict
        A dictionary containing all the defined parking spaces.

    Methods
    -------
    generate(is_update=False):
        Generates coordinates for parking spaces in the input image.
    __mouse_callback(event, x, y, flags, param):
        A callback function for mouse events.
    __handle_left_click(x, y):
        Handles left mouse clicks to define parking space coordinates.
    __handle_mouse_move(x, y):
        Handles mouse movement to show a preview of the current parking space being defined.
    __save_coordinates():
        Saves the generated coordinates to a file.
    __load_coordinates():
        Loads existing coordinates from a file.
    get_Coordinates():
        Returns the generated coordinates with an 'is_occupied' flag set to False.
    """

    KEY_RESET = ord("r")
    KEY_QUIT = ord("q")

    def __init__(self, image, path_to_saved_coordinates):
        """
        Parameters
        ----------
        image : numpy.ndarray
            The input image to generate coordinates for.
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

    def generate(self, is_update=False):
        """
        Generates coordinates for parking spaces in the input image.

        Parameters
        ----------
        is_update : bool, optional
            A flag indicating whether the generator is being used to update existing coordinates. Default is False.
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
        A callback function for mouse events.

        Parameters
        ----------
        event : int
            The type of mouse event.
        x : int
            The x-coordinate of the mouse event.
        y : int
            The y-coordinate of the mouse event.
        flags : int
            Additional flags for the mouse event.
        param : Any
            Additional parameters for the mouse event.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.__handle_left_click(x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            self.__handle_mouse_move(x, y)

    def __handle_left_click(self, x, y):
        """
        Handles left mouse clicks to define parking space coordinates.

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
        Handles mouse movement to show a preview of the current parking space being defined.

        Parameters
        ----------
        x : int
            The x-coordinate of the mouse movement.
        y : int
            The y-coordinate of the mouse movement.
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
                if mode == "a" and i <= self.loaded_id:
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
        Loads existing coordinates from a file.
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
        open(self.path_to_data, "w").close()

    def get_Coordinates(self):
        """
        Returns the generated coordinates with an 'is_occupied' flag set to False.

        Returns
        -------
        list
            A list of dictionaries containing the generated coordinates and the 'is_occupied' flag set to False.
        """
        with_occupied_status = []
        for i in self.all_coordinates:
            with_occupied_status.append(
                {"id": i, "coordinates": self.all_coordinates[i], "is_occupied": False}
            )

        return with_occupied_status
