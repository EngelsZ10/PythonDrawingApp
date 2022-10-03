from Modulos.UI import *
import sys
import pygame
import Modulos.funciones as f
import Modulos.constantes as c

colorinv = pygame.Color(0, 0, 0)
screen2 = pygame.Surface((100, 100))
screen2.fill(c.gray)
# inicializar Screen
pygame.init()
screen = pygame.display.set_mode((c.Screen["dimenciones"]))
screen2.set_colorkey(c.hotpink)
screen2.fill(c.blue)
pygame.display.set_caption("Engels Emiliano  Miranda Palacios © cpyright")
select = Boton(c.cyan, (0, 0, 100, 40), screen, texto="Select")
add = Boton(c.green, (100, 0, 120, 40), screen, texto="Add figure")
delete = Boton(c.red, (220, 0, 100, 40), screen, texto="Delete")
color_pick = Boton(c.gray, (320, 0, 100, 40), screen, texto="Color")
guardar = Boton(c.orange, (420, 0, 100, 40), screen, texto="Save")
clean = Boton(c.darckred, (520, 0, 100, 40), screen, texto="Clean")

espacio = 5
btn2 = {"w": 185, "h": 85}
btn = {"x": [260, 260 + btn2["w"] + espacio], "y": [160, 160 + btn2["h"] + espacio]}
rect = Boton(c.salmon, (btn["x"][0], btn["y"][1], btn2["w"], btn2["h"]), screen, texto="Rectangulo")
circle = Boton(c.darkorange, (btn["x"][1], btn["y"][0], btn2["w"], btn2["h"]), screen, texto="Circulo")
tria = Boton(c.pink, (btn["x"][0], btn["y"][0], btn2["w"], btn2["h"]), screen, texto="Triangulo")
line = Boton(c.hotpink, (btn["x"][1], btn["y"][1], btn2["w"], btn2["h"]), screen, texto="Linea")
botones = [rect, circle, tria, line]

origen = (0, 0)
figNum = 0
numFig = 0
tipo = "Linea"
RGB = [25, 250, 250]
pos_rgb = 3 * [2 * [4 * [0]]]
color = (RGB[0], RGB[1], RGB[2])
color_pick_on = False
adding = False
select_type = False
figCreated = [False, 0]
moving = False
moving_rgb = 3*[False]
selecting = False
selected = [False, 0]
isResizing = False
cuadro_press = [False, None]
warning = False
cleaning = False

while True:
    # eventos discretos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == pygame.BUTTON_LEFT:
            if clean.onPress(e.pos):
                warning = not warning
            if guardar.onPress(e.pos):
                f.guardar(screen)
            if select.onPress(e.pos) and not adding:
                selecting = not selecting
                selected = [False, 0]
                if selecting:
                    select.color = c.blue
                else:
                    select.color = c.cyan
            for i in range(3):
                if f.isOnPress(e.pos, pos_rgb[i][0]):
                    moving_rgb[i] = True
            if color_pick.onPress(e.pos):
                color_pick_on = not color_pick_on
                pos_rgb = 3 * [2 * [4 * [0]]]
                add.color = c.green
                select_type = False
                adding = False
            if delete.onPress(e.pos) and selected[1] and "figura" + str(selected[1]) in c.drawings:
                del c.drawings["figura" + str(selected[1])]
                selected = [False, 0]
                numFig -= 1
            if add.onPress(e.pos) and not color_pick_on and not selecting:
                if adding:
                    select_type = False
                    adding = False
                else:
                    select_type = not select_type
                if adding or select_type:
                    add.color = c.mediumpurple
                else:
                    add.color = c.green
            elif select_type:
                tipo, adding = f.selecting_type(pygame.mouse.get_pos(), botones)
                select_type = not adding
                print(tipo)
            elif adding and not color_pick.onPress(e.pos) and not color_pick_on and not selecting:
                figNum += 1
                numFig += 1
                origen = e.pos
                f.addFig(screen, tipo, origen, color, figNum, True)
                figCreated = [True, figNum]
            elif selecting:
                noneSelected = True
                if selected[0]:
                    cuadro_press = c.drawings["figura" + str(selected[1])].isCuadroPress(pygame.mouse.get_pos())
                for i in c.drawings:
                    if c.drawings[i].onPress(e.pos):
                        noneSelected = False
                        if not cuadro_press[0]:
                            selected = [True, c.drawings[i].index]
                if noneSelected and not cuadro_press[0]:
                    selected = [False, 0]
                elif selected[0]:
                    if c.drawings["figura" + str(selected[1])].onPress(e.pos):
                        moving = True
        if e.type == pygame.MOUSEMOTION and moving:
            pos = e.rel
            c.drawings["figura" + str(selected[1])].move(pos)
        if e.type == pygame.MOUSEBUTTONUP and e.button == pygame.BUTTON_LEFT:
            if figCreated[0]:
                c.drawings["figura" + str(figCreated[1])].start = False
            figCreated = [False, 0]
            moving = False
            isResizing = False
            moving_rgb = 3*[False]
    # eventos continuos
    screen.fill(c.Screen["color"])
    if pygame.mouse.get_pressed()[0] and figCreated[0]:
        c.drawings["figura" + str(figCreated[1])].size(origen, pygame.mouse.get_pos())
    add.build()
    select.build()
    delete.build()
    color_pick.build()
    guardar.build()
    clean.build()
    for i in range(3):
        if moving_rgb[i]:
            RGB[i] = f.check_sliding(pos_rgb[i], pygame.mouse.get_pos(), RGB[i])
            color = (RGB[0], RGB[1], RGB[2])
    for i in c.drawings:
        if selected[0] and c.drawings[i].index == selected[1]:
            c.drawings[i].dibuja(screen, True)
            cuadro_press = c.drawings[i].isCuadroPress(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0] and cuadro_press[0] and not isResizing:
                figCreated = [True, c.drawings[i].index]
                isResizing = True
                origen = (int(c.drawings[i].cuadroContrario(cuadro_press[1])[0]),
                          int(c.drawings[i].cuadroContrario(cuadro_press[1])[1]))
        else:
            c.drawings[i].dibuja(screen, False)
    if select_type:
        f.addfiguras(screen, (200, 200, 200), (250, 150), botones)
    elif color_pick_on:
        pos_rgb = f.color_picker(screen, color, RGB, (250, 150))
    elif warning:
        if pygame.mouse.get_pressed()[0]:
            warning, cleaning = f.cleanAll(screen, pygame.mouse.get_pos(), True)
        else:
            warning, cleaning = f.cleanAll(screen, pygame.mouse.get_pos(), False)
        if cleaning:
            figCreated = [False, 0]
    pygame.display.flip()
