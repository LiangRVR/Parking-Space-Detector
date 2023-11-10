from util.Parking_Space_Detector import ParkingSpaceDetector


def main():
    path_to_data = "./data/coordinates.yml"
    video_path = "./parking1.mp4"
    parking_space_detector = ParkingSpaceDetector(video_path, path_to_data, draw_cars=False)
    parking_space_detector.check_parking_spot_occupied()


if __name__ == "__main__":
    main()
