import pygame

class dummyText:
    def load(self): pass

def loadText(text, fontName, fontSize, fontColor):
    try:
        myfont = pygame.font.SysFont(fontName, fontSize)
        return myfont.render(text, True, fontColor)
    except pygame.error:
        print('Warning, unable to load,', text)
    return dummyText()