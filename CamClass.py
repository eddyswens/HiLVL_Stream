import cv2
import pickle
import Config
import numpy as np


class Camera:

    def __init__(self, height, width, url, file_name):
        self.RTSP_URL = url
        self.height = height
        self.width = width
        self.cam_sets_file_name = file_name
        self.cap = cv2.VideoCapture(self.RTSP_URL, cv2.CAP_FFMPEG) # cv2.CAP_FFMPEG
        self.points_rv_tv = Config.POINTS
        self.zero_dist_coefs = np.zeros((4, 1))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        try:
            params = open(self.cam_sets_file_name, 'rb')
            self.main_rvec, self.main_tvec, self.mapx, self.mapy, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs = pickle.load(params)
            params.close()
        except:
            # self.calibration()
            self.get_new_rvec_tvec()
            self.storage_new_settings()

        # Инициализация кольца
        self.radius = Config.RAD
        self.num_points = Config.NUM_POINTS
        self.theta = np.linspace(0, 2 * np.pi, self.num_points)


    def get_std_frame(self):
        ret, self.std_frame = self.cap.read()

        if not ret:
            print("failed to grab frame")
            return None

        return self.std_frame


    def get_undist_frame(self):
        self.fixed_frame = cv2.remap(self.get_std_frame(), self.mapx, self.mapy, cv2.INTER_LINEAR)
        return self.fixed_frame


    def storage_new_settings(self):
        with open(self.cam_sets_file_name, 'wb') as params:  # Записываем значения параметров в файл
            list_of_parameters = [self.main_rvec, self.main_tvec, self.mapx, self.mapy, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs]
            pickle.dump(list_of_parameters, params)


    def calibration(self, imgpoints=None, more_info=0):
        shots = Config.NUMBER_OF_SHOTS
        board_size = Config.BOARD_SIZE  # Определение размеров шахматной доски
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objpoints = []  # Создание вектора для хранения векторов трехмерных точек для каждого изображения шахматной доски
        objp = np.zeros((1, board_size[0] * board_size[1], 3), np.float32)  # Определение мировых координат для 3D точек
        objp[0, :, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)
        gray = None

        if not imgpoints:
            imgpoints = []  # Создание вектора для хранения векторов 2D точек для каждого изображения шахматной доски
            while shots:
                frame = self.get_std_frame().copy()
                cv2.imshow("Calibration frame", frame)

                if cv2.waitKey(1) & 0xFF == ord('p'):
                    if gray is None:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    ret, corners = cv2.findChessboardCorners(gray, board_size,
                                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

                    if ret:
                        shots -= 1
                        objpoints.append(objp)
                        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # Уточнение положений углов
                        imgpoints.append(corners2)
                        frame = cv2.drawChessboardCorners(frame, board_size, corners2, ret)
                        cv2.imshow('frame', frame)
                        cv2.waitKey(1000)
                        cv2.destroyWindow('frame')

            h, w = frame.shape[:2]
            cv2.destroyAllWindows()

        ret, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                                                               gray.shape[::-1], None,
                                                                                               None)
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.camera_matrix, self.dist_coefs, None, None, (w, h), 5)
        self.storage_new_settings()

        if more_info:
            print("Camera matrix:\n", self.camera_matrix)
            print("dist:\n", self.dist_coefs)
            print("rvecs:\n", self.rvecs)
            print("tvecs:\n", self.tvecs)

    def get_new_rvec_tvec(self):
        self.points_rv_tv = Config.POINTS
        cv2.namedWindow('LiveCam')
        arr3d = np.array([[[1.019, -1.370, 0],
                           [-1.430, -1.419, 0],
                           [-1.478, 1.214, 0],
                           [1.345, 1.277, 0],
                           [2.675, -0.032, 1],
                           [-2.1, -0.158, 1]
                           ]], dtype=float)
        arr2d = np.zeros((self.points_rv_tv, 2))

        def mouse_click_handler(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                arr2d[-self.points_rv_tv] = [x, y]
                self.points_rv_tv -= 1
                print(x, y)

        cv2.setMouseCallback('LiveCam', mouse_click_handler)

        while self.points_rv_tv:
            frame = self.get_undist_frame()
            cv2.imshow('LiveCam', frame)

            if cv2.waitKey(1) & 0xFF == ord('x'):
                cv2.destroyAllWindows()
                break

        cv2.destroyAllWindows()
        ret, self.main_rvec, self.main_tvec = cv2.solvePnP(arr3d, arr2d, self.camera_matrix, self.zero_dist_coefs)
        if ret:
            self.storage_new_settings()


    def draw_circle(self, center_x, center_y, center_z, draw=0, frame=None):
        radius = self.radius
        theta = self.theta

        x = radius * np.cos(theta) + center_x
        y = radius * np.sin(theta) + center_y
        z = np.full_like(x, center_z)

        points_3d = np.column_stack((x, y, z))
        points_2d, _ = cv2.projectPoints(points_3d, self.main_rvec, self.main_tvec, self.camera_matrix,
                                         self.zero_dist_coefs)
        circle_points = []

        for point in points_2d:
            x, y = point.ravel()
            if draw:
                cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)

            circle_points.append([x, y])
        return circle_points

