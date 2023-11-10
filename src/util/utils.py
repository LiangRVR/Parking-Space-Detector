import cv2
from util.colors import COLOR_BLUE, COLOR_RED

def draw_rectangles(points, image, is_occupied=False):
    """
    Draws a rectangle on the given image using the provided points.

    Args:
        points (list): A list of (x, y) tuples representing the corners of the rectangle.
        image (numpy.ndarray): The image on which to draw the rectangle.
        is_occupied (bool, optional): A flag indicating whether the parking space is occupied. Defaults to False.
    """
    point_1 = points[0]
    color = COLOR_BLUE if not is_occupied else COLOR_RED
    for i in range(1, len(points)):
        cv2.line(image, point_1, points[i], color, 2)
        point_1 = points[i]
    cv2.line(image, point_1, points[0], color, 2)
