import cv2
from util.colors import COLOR_BLUE, COLOR_RED

def draw_rectangles(points, image, is_occupied = False):
    point_1 = points[0]
    color = COLOR_BLUE if not is_occupied else COLOR_RED
    print(color)
    for i in range(1, len(points)):
        cv2.line(image, point_1, points[i], color, 2)
        point_1 = points[i]
    cv2.line(image, point_1, points[0], color, 2)
