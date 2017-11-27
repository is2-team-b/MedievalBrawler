import pygame

def draw_text(screen, text, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name,18)
    text_surface =  font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

class dummyText:
    def load(self): pass


def loadText(text, fontName, fontSize, fontColor):
    try:
        myfont = pygame.font.SysFont(fontName, fontSize)
        return myfont.render(text, True, fontColor)
    except pygame.error:
        print('Warning, unable to load,', text)
    return dummyText()
