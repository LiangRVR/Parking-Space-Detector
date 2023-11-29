from Parking_Space_Detector import ParkingSpaceDetector


def main():
    """
    Runs the Parking Space Detector program with the specified video and data paths.
    """
    path_to_data = "./data/coordinates1.yml"
    video_path = "./parking1.mp4"
    parking_space_detector = ParkingSpaceDetector(
        video_path, path_to_data, update_coordinate=True, draw_cars=True
    )
    parking_space_detector.check_parking_spot_occupied()


if __name__ == "__main__":
    main()
