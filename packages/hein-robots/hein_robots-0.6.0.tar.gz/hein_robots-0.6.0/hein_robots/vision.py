from dataclasses import dataclass
from typing import Dict, List
import cv2
import numpy as np
from pupil_apriltags import Detector, Detection
from hein_robots.robotics import Location, Cartesian, Orientation


class Camera:
    def __init__(self, camera_matrix: Dict, distortion_coefficients: Dict, camera_index=0, connect=True, **kwargs):
        self.camera_matrix = np.array(camera_matrix['data']).reshape(3, 3)
        self.distortion_coefficients = np.array(distortion_coefficients['data'])
        self.camera_index = camera_index
        self.camera = None

        if connect:
            self.connect()

    def connect(self):
        self.camera = cv2.VideoCapture(self.camera_index)

    def get_image(self) -> np.array:
        ret, image = self.camera.read()

        if not ret:
            raise CameraError(f'Unable to read image from camera {self.camera_index}')

        return image


class MarkerDetector:
    def __init__(self, camera: Camera, default_marker_size: float=0.04, marker_sizes: Dict[int, float] = {}, draw_axes=True, **kwargs):
        self.camera = camera
        self.draw_axes = draw_axes
        self.default_marker_size = default_marker_size
        self.tag_sizes = marker_sizes

    def get_marker_size(self, tag_id: int):
        return self.tag_sizes.get(tag_id, self.default_marker_size)

    def detect(self, image: np.array, camera_location=Location()) -> List['MarkerDetection']:
        pass

    def draw_marker_axes(self, image: np.array, marker: 'MarkerDetection'):
        cv2.drawFrameAxes(image, self.camera.camera_matrix, self.camera.distortion_coefficients,
                          marker.np_rotation, marker.np_translation, marker.tag_size)

        text_location = np.float32([[.01, .01, 0]]).reshape(-1, 3)
        projected_points, jacobian = cv2.projectPoints(text_location, marker.np_rotation, marker.np_translation,
                                                       self.camera.camera_matrix, self.camera.distortion_coefficients)

        text = f'#{marker.id} ({marker.location.x:.2f}, {marker.location.y:.2f}, {marker.location.z:.2f})'
        cv2.putText(image, text, projected_points[0][0].astype(int), cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 0, 255), 3, cv2.LINE_AA)


class ArucoMarkerDetector(MarkerDetector):
    def __init__(self, families: str, **kwargs):
        super().__init__(**kwargs)
        aruco_dict = cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, families))
        aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    def detect(self, image: np.array, camera_location=Location()) -> List['MarkerDetection']:
        corners, ids, rejected = self.detector.detectMarkers(image)

        if ids is None:
            return []

        return [self.build_detection(image, marker_corners, marker_id, camera_location)
                for marker_corners, marker_id in zip(corners, ids.flatten())]

    def build_detection(self, image: np.array, corners: np.array, marker_id: int, camera_location: Location):
        marker_size = self.get_marker_size(marker_id)
        object_points = np.mat([[0, 0, 0], [marker_size, 0, 0], [marker_size, marker_size, 0], [0, marker_size, 0]])
        ret, rotation, translation = cv2.solvePnP(object_points,
                                                  corners,
                                                  self.camera.camera_matrix,
                                                  self.camera.distortion_coefficients,
                                                  False,
                                                  cv2.SOLVEPNP_IPPE_SQUARE)

        if not ret:
            raise MarkerDetectorError(f'Error estimating marker location: {marker_id}')

        marker_location_camera = Location(Cartesian(*translation.reshape(3).tolist()),
                                          Orientation(*rotation.reshape(3).tolist()))
        marker_location_world = marker_location_camera * camera_location

        marker = MarkerDetection(id=marker_id,
                                 tag_size=marker_size,
                                 location=marker_location_world,
                                 location_camera=marker_location_camera,
                                 np_translation=translation,
                                 np_rotation=rotation)

        if self.draw_axes:
            self.draw_marker_axes(image, marker)

        return marker


class AprilTagsMarkerDetector(MarkerDetector):
    def __init__(self, families='tag36h11', **kwargs):
        super().__init__(**kwargs)
        self.detector = Detector(families=families, quad_decimate=1.0)

    def detect(self, image: np.array, camera_location=Location()) -> List['MarkerDetection']:
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        tags = self.detector.detect(grayscale_image)

        return [self.build_detection(image, camera_location, tag) for tag in tags]

    def build_detection(self, image: np.array, camera_location: Location, tag: Detection) -> 'MarkerDetection':
        tag_size = self.get_marker_size(tag.tag_id)
        tag_corners = tag.corners
        object_points = np.mat([[0, 0, 0], [tag_size, 0, 0], [tag_size, tag_size, 0], [0, tag_size, 0]])
        ret, rotation, translation = cv2.solvePnP(object_points,
                                                  tag_corners,
                                                  self.camera.camera_matrix,
                                                  self.camera.distortion_coefficients)

        if not ret:
            raise MarkerDetectorError(f'Error estimating marker location: {tag}')

        marker_location_camera = Location(Cartesian(*translation.reshape(3).tolist()),
                                          Orientation(*rotation.reshape(3).tolist()))
        marker_location_world = marker_location_camera.relative_to(camera_location.inverse)
        marker = MarkerDetection(id=tag.tag_id,
                                 tag_size=tag_size,
                                 location=marker_location_world,
                                 location_camera=marker_location_camera,
                                 np_translation=translation,
                                 np_rotation=rotation)

        # draw axes and tag id if we are given an image to draw on
        if self.draw_axes:
            self.draw_marker_axes(image, marker)

        return marker


@dataclass
class MarkerDetection:
    id: int
    tag_size: float
    location_camera: Location
    location: Location
    np_translation: np.array
    np_rotation: np.array


class CameraError(Exception):
    pass


class MarkerDetectorError(Exception):
    pass
