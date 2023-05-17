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
        self.cap = cv2.VideoCapture(self.RTSP_URL, cv2.CAP_FFMPEG)
        self.points_rv_tv = Config.POINTS
        self.zero_dist_coefs = np.zeros((4, 1))

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        params = open(self.cam_sets_file_name, 'rb')
        self.mapx, self.mapy, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs = pickle.load(params)
        params.close()


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


    def Calibration(self, more_info=0):
        shots = Config.NUMBER_OF_SHOTS
        board_size = Config.BOARD_SIZE  # Определение размеров шахматной доски
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        objpoints = []  # Создание вектора для хранения векторов трехмерных точек для каждого изображения шахматной доски
        imgpoints = []  # Создание вектора для хранения векторов 2D точек для каждого изображения шахматной доски

        objp = np.zeros((1, board_size[0] * board_size[1], 3), np.float32)  # Определение мировых координат для 3D точек
        objp[0, :, :2] = np.mgrid[0:board_size[0], 0:board_size[1]].T.reshape(-1, 2)

        while shots:
            frame = self.get_std_frame().copy()
            cv2.imshow("Calibration frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('p'):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ret, corners = cv2.findChessboardCorners(gray, board_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

                if ret == True:
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


        ret, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (w, h), 0, (w, h))  # alpha 0/1
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.camera_matrix, self.dist_coefs, None, None, (w, h), 5)

        list_of_parameters = [self.mapx, self.mapy, self.camera_matrix, self.dist_coefs, self.rvecs, self.tvecs]
        params = open(self.cam_sets_file_name, 'wb')  # Записываем значения mapx mapy в файл
        pickle.dump(list_of_parameters, params)
        params.close()

        del list_of_parameters

        if more_info:
            print("Camera matrix : \n")
            print(self.camera_matrix)
            print("dist : \n")
            print(self.dist_coefs)
            print("rvecs : \n")
            print(self.rvecs)
            print("tvecs : \n")
            print(self.tvecs)


    def get_new_Rvec_Tvec(self):
        self.points_rv_tv = Config.POINTS #Количество точек как атрибут класса - чтобы иметь к ней доступ из любой функции
        cv2.namedWindow('LiveCam')
        arr3d = np.array([[[0, 0, 0],
                           [9, 0, 0],
                           [9, 0, 1],
                           [9, 7, 0],
                           [0, 7, 0],
                           [0, 7, 1]]], dtype=float)
        arr2d = np.zeros((self.points_rv_tv, 2))

        def MouseClkHandler(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                arr2d[-self.points_rv_tv] = [x, y]
                self.points_rv_tv -= 1
                print(x, y)

        cv2.setMouseCallback('LiveCam', MouseClkHandler)

        while self.points_rv_tv:
            frame = self.get_undist_frame()
            cv2.imshow('LiveCam', frame)

            if cv2.waitKey(1) & 0xFF == ord('x'):
                cv2.destroyAllWindows()
                break

        cv2.destroyAllWindows()

        _, self.main_rvec, self.main_tvec = cv2.solvePnP(arr3d, arr2d, self.camera_matrix, self.zero_dist_coefs)


    def draw_circle(self, frame, center_x, center_y, center_z):

        x = self.radius * np.cos(self.theta) + center_x
        y = self.radius * np.sin(self.theta) + center_y
        # z = np.zeros_like(x)  # Все точки лежат на плоскости z = 0
        z = np.zeros_like(x) + center_z

        # Перевод 3D координат в формат OpenCV
        points_3d = np.vstack((x, y, z)).T
        points_3d = np.expand_dims(points_3d, axis=1)

        points_2d, _ = cv2.projectPoints(points_3d, self.main_rvec, self.main_tvec, self.camera_matrix, self.zero_dist_coefs)

        for point in points_2d:
            x, y = point.ravel()
            cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)