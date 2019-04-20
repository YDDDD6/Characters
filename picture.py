from PIL import Image
import pygame
from pygame.locals import *
import time

file = '1.jpg'
image = Image.open(file)
print(image.size)
picture_rgb = []

def Get_Char():
    pass

for x in range(image.width):
    col_rgb = []
    for y in range(image.height):
        rgb_im = image.convert('RGB')
        r, g, b = rgb_im.getpixel((x, y))
        col_rgb.append((r, g, b))
    picture_rgb.append(col_rgb)
'''
for x in range(image.width):
    for y in range(image.height):
        print(picture_rgb[x][y],end='')
    print()
'''
'''
while True:
    # 还原图片
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()
        if event.type == QUIT:
            exit()
    for x in range(image.width):
        for y in range(image.height):
            pygame.draw.line(screen, picture_rgb[x][y], (x, y), (x, y))
    pygame.display.update()
'''
