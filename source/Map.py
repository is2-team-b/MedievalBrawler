
from pygame.locals import *

class Map:
    def __init__(self, name, background, walls_list, water_list, respawn_list, flag_respawn_list):
        self.name = name  # name as displayed in the options screen
        self.background = background  # file with background picture
        self.walls = walls_list  # a list of Rect() objects
        self.water = water_list  # a list of Rect() objects
        self.respawnpoints = respawn_list
        self.flagrespawnpoints = flag_respawn_list


class MapManager:
    def __init__(self):
        self.maps = [Map("River", "river.png",
                             [Rect(0, 0, 100, 22), Rect(0, 22, 22, 55), Rect(0, 77, 100, 22),
                              Rect(0, 370, 22, 110), Rect(22, 445, 110, 35), Rect(130, 370, 25, 100),
                              Rect(580, 0, 45, 52), Rect(625, 0, 25, 90), Rect(650, 0, 50 ,20), Rect(700, 0, 30, 90),
                              Rect(600, 698, 30, 64), Rect(630, 670, 27, 92), Rect(657, 742, 53, 20), Rect(710, 670, 27, 92), Rect(737, 698, 30, 64),
                              Rect(670, 333, 113,33), Rect(670,366,40,54),Rect(685,420,98,33),
                              Rect(1275,635,45,40), Rect(1210,675,110,25), Rect(1295,700,25,50), Rect(1212,750,108,12)],
                             [Rect(255, 440, 114, 271),Rect(197, 450, 97, 11),Rect(0, 465, 288,297),
                              Rect(511, 433, 90, 77),Rect(601, 433, 46, 40),Rect(526, 250, 129, 182),
                              Rect(551, 212, 248, 38),Rect(664, 250, 137, 51),Rect(800, 200, 163, 84),
                              Rect(961, 201, 29, 67),
                              Rect(1152, 0, 168, 82),Rect(1152, 82, 112, 28),Rect(870, 39, 282, 85),
                              Rect(850, 58, 20, 66),Rect(814, 86, 36, 38)],
                              [[380,712,90], [5,7,0], [745,717,180],[5,717,0],[745,7,180],[380,10,270]],
                              []),
                     Map("Ocean Wall", "ocean_wall.jpg",
                             [Rect(0, 0, 1024, 1), Rect(0, 0, 1, 768), Rect(795, 0, 8, 768), Rect(0, 763, 1024, 1), Rect(1023, 0, 1, 768),
                              Rect(1, 60, 100, 150), Rect(1, 545, 100, 150), Rect(700, 60, 100, 150), Rect(700,545,100,150),
                              Rect(212, 0, 160, 80), Rect(440, 0, 160, 80), Rect(212, 688, 160, 80), Rect(440, 688, 160, 80),
                              Rect(310, 145, 180, 140), Rect(310, 483, 180, 140), Rect(70,279,180,210), Rect(550,279,180,210)],
                             [], [[380,712,90], [5,7,0], [745,717,180], [5,717,0], [745,7,180], [380,10,270]],[])]



