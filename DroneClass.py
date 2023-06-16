import Config
import dataclasses
import threading
from piosdk.piosdk import Pioneer  # Импортируем класс Pioneer
import time

if Config.SIMULATION_ENABLE:
    class Drone:
        def __init__(self):
            self.pos = [[[0, 0, 0]]]
            self.th = threading.Thread(target=self.move)
            self.th.start()



        def move(self):
            while True:
                while self.pos[0][0][0] < 9:
                    time.sleep(0.05)
                    self.pos[0][0][0] += 0.05
                    # self.pos[0][0][2] += 0.01

                    print(self.pos[0][0][0])
                self.pos[0][0][1] += 1

                while self.pos[0][0][0] > 0:
                    time.sleep(0.05)
                    self.pos[0][0][0] -= 0.05
                    # self.pos[0][0][2] -= 0.01
                    print(self.pos[0][0][0])
                self.pos[0][0][1] += 1

else:
    # Классы для хранения настроек подключения
    @dataclasses.dataclass
    class IpPort:
        ip: str
        port: int


    class DroneConnectingData:
        drone0: IpPort = IpPort(ip="10.10.33.48", port=5656)

    drone = Pioneer(ip=DroneConnectingData.drone0.ip, mavlink_port=DroneConnectingData.drone0.port, logger=False)
    prev_pos = [0, 0, 0]

    def get_pos():
        global prev_pos
        pos = drone.get_local_position_lps()
        if pos is not None:
            # print(pos)
            prev_pos = pos
            return pos
        else:
            return prev_pos


if __name__ == '__main__':
    while True:
        print(get_pos())