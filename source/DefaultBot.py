import random
import pygame

from source import GameData

def DefaultBot(character,time):
    action = random.random() * 100
    if action < 20:
        if random.random() < 0.5:
            character.moveBot("up",character)
        else:
            character.shoot(time)
    if 20 < action < 40:
        if random.random() < 0.5:
            character.moveBot("left", character)
        else:
            character.shoot(time)
    if 40 < action < 60:
        if random.random() < 0.5:
            character.moveBot("right", character)
        else:

            character.shoot(time)
    if 60 < action < 80:
        if random.random() < 0.5:
            character.moveBot("down", character)
        else:
            character.shoot(time)
    if action == 40:
        for t in range(0, 6):
            character.moveBot("left", character)
            character.shoot(time)
    if action == 50:
        for t in range(0, 6):
            character.moveBot("right", character)
            character.shoot(time)
    # if action == 45:
    #     character.moveBot("left", character)
    #     character.shoot(time)
    #     character.moveBot("up", character)
    #     character.moveBot("right", character)
    #     character.shoot(time)
    #     character.moveBot("down", character)
    #     character.shoot(time)


    # # Avoid walls in a random direction
    # for wall in GameData.Game.get_instance().battleground.walls:
    #     if wall.colliderect(character.rect):
    #         if random.random() < 0.5:
    #             for i in range(0, int(random.random() * 450 )):
    #                 character.moveBot("left", character)
    #                 character.shoot(time)
    #             # tank.command_queue.append("flush")
    #         else:
    #             for i in range(0, int(random.random() * 450 )):
    #                 character.moveBot("right", character)
    #                 character.shoot(time)
    #             # tank.command_queue.append("flush")
    #
    # # Avoid water in a random direction
    # for pool in GameData.Game.get_instance().battleground.water:
    #     if pool.colliderect(character.rect):
    #         if random.random() < 0.5:
    #             for i in range(0, int(random.random() * 450 )):
    #                 character.moveBot("left", character)
    #                 character.shoot(time)
    #             # tank.command_queue.append("flush")
    #         else:
    #             for i in range(0, int(random.random() * 450 )):
    #                 character.moveBot("right", character)
    #                 character.shoot(time)
    #             # tank.command_queue.append("flush")

    # # Avoid borders and turn towards the centre of the arena
    # if (character.y < 60) and (character.angle < 180):
    #     if character.x < 400:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # character.command_queue.append("flush")
    #     else:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # character.command_queue.append("flush")
    # elif character.y > 668 and (character.angle > 180):
    #     if character.x < 400:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # tank.command_queue.append("flush")
    #     else:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             character.command_queue.append("pass")
    #         # character.command_queue.append("flush")
    # elif character.x > 705 and ((character.angle < 90) or (character.angle > 270)):
    #     if character.y < 400:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             character.command_queue.append("pass")
    #         # character.command_queue.append("flush")
    #     else:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # character.command_queue.append("flush")
    # elif character.x < 60 and (90 < character.angle < 270):
    #     if character.y < 400:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # tank.command_queue.append("flush")
    #     else:
    #         for i in range(0, int(120 )):
    #             character.move()
    #         character.shoot()
    #         for i in range(0, int(10)):
    #             pass
    #         # tank.command_queue.append("flush")
