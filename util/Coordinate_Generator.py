import cv2

from colors import COLOR_RED, COLOR_GREEN, COLOR_BLUE


class CoordinateGenerator:

    def __init__(self, image, output):
        self.original_image = image.copy()
        self.output_file = output

        self.preview_image = None
        self.current_point = (-1, -1)
        self.first_point = (-1, -1)
        self.num_points = 0

    def generate(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.__mouse_callback)

        while True:

            if self.preview_image is None:
                cv2.imshow('image', self.original_image)
            else:
                cv2.imshow('image', self.preview_image)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
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
            cv2.line(self.original_image, self.current_point,
                     (x, y), COLOR_BLUE, 1)

        self.current_point = (x, y)
        self.num_points += 1

        if self.num_points == 4:
            self.num_points = 0
            cv2.line(self.original_image, self.current_point,
                     self.first_point, COLOR_BLUE, 1)

    def __handle_mouse_move(self, x, y):
        if self.num_points > 0:
            self.preview_image = self.original_image.copy()
            cv2.line(self.preview_image, self.current_point,
                     (x, y), COLOR_GREEN, 1)
        else:
            self.preview_image = None
