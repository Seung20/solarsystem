import pygame
import numpy as np
import imageio.v3 as iio
from timeit import default_timer as timer

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()


def imgRotate(img, degree, corx = -1, cory = -1):
    c = np.cos(np.deg2rad(degree))
    s = np.sin(np.deg2rad(degree))


    imgr3 =np.zeros(img.shape, dtype='uint8')
    if img.shape[2] == 4:
        imgr3[:,:,3] = 255

    if corx == -1 and cory == -1:
        corx = img.shape[1] / 2.
        cory = img.shape[0] / 2.


    for iyp in range(imgr3.shape[0]):
        for ixp in range(imgr3.shape[1]):
            # inverse rotation
            x = c * (ixp-corx) + s * (iyp - cory) + corx
            y = -s * (ixp-corx) + c * (iyp - cory) + cory

            ix = int(x)
            iy = int(y)

            if ix < 0 or ix >= img.shape[1] or iy < 0 or iy >= img.shape[0]:
                continue
                
            color = img[iy, ix]
            imgr3[iyp, ixp] = color

    return imgr3
    

def yearrotation(deg, positionx, positiony, centerx, centery):
    c = np.cos(np.deg2rad(deg))
    s = np.sin(np.deg2rad(deg))
    
    R = np.array( [[ c, -s], [s, c] ] )
    po = [positionx, positiony]
    cor = [centerx, centery]

    for i in range(2):
        po[i] = po[i] - cor[i]
    po = R @ po
    for i in range(2):
        po[i] = po[i] + cor[i]

    return po

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = display.get_size()


img_sun = iio.imread("img/sun.png")
img_venus = iio.imread("img/venus.png")
img_earth = iio.imread("img/earth.png")
img_saturn = iio.imread("img/saturn.png")
img_moon = iio.imread("img/moon.png")
img_titan = iio.imread("img/Titan.png")
img_starship = iio.imread("img/starship.png")


img_sun = img_sun[:,:,:3]
img_venus = img_venus[:,:,:3]
img_earth = img_earth[:,:,:3]
img_saturn = img_saturn[:,:,:3]

img_moon = img_moon[:,:,:3]
img_titan = img_titan[:,:,:3]
img_starship = img_starship[:,:,:3]


init_time = timer()
frames_displayed = 0

running = True
#자전 속도 및 각도
degree = 0
degree_s = 0
degree_m = 0
degree_tt = 0
degree_v = 0
#공전 속도 및 각도
venus_yd = 0
earth_yd =0
saturn_yd = 0

moon_yd = 0
titan_yd = 0
starship_yd = 30


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #자전 속도 설정
    degree += 1
    degree_s += 2
    degree_v += 0.004
    degree_m += 0.3
    degree_tt += 0.6

    imgr_earth = imgRotate(img_earth, degree)
    imgr_saturn = imgRotate(img_saturn, degree_s)
    imgr_moon = imgRotate(img_moon, degree_m)
    imgr_titan = imgRotate(img_titan, degree_tt)



    surf_s = pygame.surfarray.make_surface(img_sun)
    surf_v = pygame.surfarray.make_surface(img_venus)

    surf_m = pygame.surfarray.make_surface(imgr_moon)
    surf_tt = pygame.surfarray.make_surface(imgr_titan)

    surf_e = pygame.surfarray.make_surface(imgr_earth)
    surf_t = pygame.surfarray.make_surface(imgr_saturn)

    surf_starship = pygame.surfarray.make_surface(img_starship)


    center_x = 1000
    center_y = 500

    # 공전 속도
    venus_yd += 1.6
    earth_yd += 1
    saturn_yd += 0.03

    starship_yd += 0.02

    moon_yd += 3
    titan_yd += 3
    #공전 위치, 공전 속도 설정
    venus_po = yearrotation(venus_yd, (center_x - 100), 500, center_x, center_y)
    earth_po = yearrotation(earth_yd, (center_x - 300), 600, center_x, center_y)
    saturn_po = yearrotation(saturn_yd, (center_x - 600), 800, center_x, center_y)
    star_po = yearrotation(starship_yd, (center_x - 700), 800, center_x, center_y)

    moon_po = yearrotation(moon_yd, (earth_po[0]-100), earth_po[1], earth_po[0], earth_po[1])
    titan_po = yearrotation(titan_yd, (saturn_po[0] - 200), saturn_po[1], saturn_po[0], saturn_po[1])



    display.fill(BLACK)
    for i in range(5):
         pygame.draw.circle(display, WHITE, [np.random.randint(0,width), np.random.randint(0,height)], 1)

    display.blit(surf_v,venus_po)
    display.blit(surf_e,earth_po)
    display.blit(surf_t,saturn_po)
    display.blit(surf_tt,titan_po)
    display.blit(surf_m,moon_po)
    display.blit(surf_starship,star_po)
    display.blit(surf_s,[center_x, center_y])
    

    pygame.display.flip()

    frames_displayed+=1
    clock.tick(60)

pygame.quit()
