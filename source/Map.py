from pygame.locals import *

class Map:
    def __init__(self, name, background, walls_list, water_list, respawn_list, enemy_respawn_list):
        self.name = name  # name as displayed in the options screen
        self.background = background  # file with background picture
        self.walls = walls_list  # a list of Rect() objects
        self.water = water_list  # a list of Rect() objects
        self.respawnpoints = respawn_list
        self.enemyrespawnpoints = enemy_respawn_list


class MapManager:
    def __init__(self):
        self.maps = [Map("River", "river.png",
                             [Rect(0, 0, 100, 15), Rect(0, 15, 22, 85), Rect(0, 87, 100, 12),
                              Rect(0, 370, 22, 110), Rect(22, 445, 110, 35), Rect(130, 370, 25, 100),
                              Rect(580, 0, 45, 52), Rect(625, 0, 15, 90), Rect(640, 0, 70 ,20), Rect(710, 0, 15, 90),
                              Rect(600, 698, 30, 64), Rect(630, 670, 20, 92), Rect(647, 747, 73, 25), Rect(720, 670, 20, 92), Rect(737, 698, 30, 64),
                              Rect(670, 333, 113,25), Rect(670,358,40,70),Rect(685,428,98,25),
                              Rect(1275,635,45,40), Rect(1210,675,110,25), Rect(1295,700,25,50), Rect(1212,750,108,12)],
                             [Rect(255, 440, 114, 271),Rect(197, 450, 97, 11),Rect(0, 465, 288,297),
                              Rect(511, 433, 90, 77),Rect(601, 433, 46, 40),Rect(526, 250, 129, 182),
                              Rect(551, 212, 248, 38),Rect(664, 250, 137, 51),Rect(800, 200, 163, 84),
                              Rect(961, 201, 29, 67),
                              Rect(1152, 0, 168, 82),Rect(1152, 82, 112, 28),Rect(870, 39, 282, 85),
                              Rect(850, 58, 20, 66),Rect(814, 86, 36, 38)],
                              (50,150),
                              [[Rect(652,28,60,40),0],[Rect(250,250,60,40),0]]),
                     Map("Ocean Wall", "ocean_wall.png",
                             [Rect(181, 246, 159, 24), Rect(310, 246, 27, 97), Rect(179, 246, 25, 103),
                              Rect(1279, 629, 41, 73), Rect(631, 682, 21, 80),Rect(592, 725, 60, 37), Rect(723, 683, 18, 78), Rect(741, 694, 29, 69),
                              Rect(3, 661, 84, 23), Rect(82, 676, 83, 15), Rect(0, 701, 12, 62),
                              Rect(586,209,82,45), Rect(586, 214, 10, 142), Rect(586, 305, 88, 57),
                              Rect(1189, 60, 131, 49),
                              Rect(1207, 681, 115, 20), Rect(1279, 629, 41, 73)],
                             [Rect(1, 218, 101, 380), Rect(74, 225, 81, 353),Rect(148, 201, 226, 23), Rect(364, 210, 39, 165), Rect(321, 377, 355, 142),
                              Rect(488, 203, 101, 31), Rect(448, 81, 72, 120), Rect(498, 56, 201, 33), Rect(692, 4, 158, 53)],
                             (238,298),
                             [[Rect(33,705,60,40),0],
                              [Rect(656 ,695,50,40),0],
                              [Rect(1216, 8, 60, 40), 0],
                              [Rect(1203, 713, 60, 40), 0],
                              [Rect(600, 255, 60, 40), 0]])]

    def getMapByFilename(self,Name):
         self.maps