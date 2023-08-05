import pygame
pygame.init()


class Entity:
    def __init__(self):
        self.frame = -1

    def createAnimation(self, frameCycle:tuple,size=(50,50)):
        self.images = []
        for i in frameCycle:
            img = pygame.image.load(i)
            img = pygame.transform.scale(img,size)
            self.images.append(img)


    def Animate(self,screen,Speed:int):
        pygame.time.delay(Speed)
        if self.frame != len(self.images)-1:
            self.frame += 1
        else:
            self.frame = -1
        screen.blit(self.images[self.frame],self.pos)
