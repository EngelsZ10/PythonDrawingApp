import Modulos.UI as UI
import Modulos.constantes as c
import pygame


def cleanAll(screen, pos, press):
    rectBorder(screen, (200, 200, 200), (250, 170, 400, 180), 5)
    myfont = pygame.font.SysFont("rubik mono one", 40, bold=True)
    sure = UI.Boton(c.red, (253, 296, 196, 51), screen, texto="Clean All")
    cancel = UI.Boton(c.green, (450, 296, 197, 51), screen, texto="Keep All")
    text = myfont.render(f"¿Quieres eliminar todo?", True, c.black)
    screen.blit(text, (261, 220))
    sure.build()
    cancel.build()
    if sure.onPress(pos) and press:
        c.drawings = {}
        return False, True
    elif cancel.onPress(pos) and press:
        return False, False
    else:
        return True, False


def guardar(screen):
    try:
        image = open("imageNum.txt", "r")
    except:
        num = 0
    else:
        num = image.read()
        try:
            num = int(num) + 1
        except:
            num = 0
        image.close()
    image = open("imageNum.txt", "w")
    image.write(str(num))
    image.close()
    guardarImagen(screen, num)


def guardarImagen(screen, num):
    pygame.image.save(screen, f"image{num}.jpg")


def selecting_type(pos, botones):
    for boton in botones:
        if boton.onPress(pos):
            return boton.texto, True
    return "Rectangulo", False


def check_sliding(pos_rgb, pos, default):
    if entre("x", pos, pos_rgb[1]):
        pos_rgb[0][0] = pos[0]
        return pos[0] - pos_rgb[1][0]
    return default


def rectBorder(screen, color, dimenciones, b, br=0):
    pygame.draw.rect(screen, color, dimenciones, border_radius=br)
    pygame.draw.rect(screen, c.black, dimenciones, b, border_radius=br)


def addfiguras(screen, color, pos, botones):
    rectBorder(screen, color, (pos, (400, 200)), 5)
    for i in botones:
        i.build()


def color_picker(screen, color, rgb, pos):
    myfont = pygame.font.SysFont("rubik mono one", 40, bold=True)
    myfont2 = pygame.font.SysFont("rubik mono one", 32, )
    rectBorder(screen, (200, 200, 200), (pos[0], pos[1], 400, 300), 5, br=25)
    pos_r = slider(screen, (pos[0] + 103, pos[1] + 50, 0, 0), c.red, f"R", myfont, rgb[0])
    pos_g = slider(screen, (pos[0] + 103, pos[1] + 100, 0, 0), c.green, f"G", myfont, rgb[1])
    pos_b = slider(screen, (pos[0] + 103, pos[1] + 150, 0, 0), c.blue, f"B", myfont, rgb[2])
    rectBorder(screen, color, (pos[0] + 42, pos[1] + 210, 70, 50), 3)
    text = myfont2.render(f"R = {rgb[0]}, G = {rgb[1]}, B = {rgb[2]}", True, c.black)
    screen.blit(text, (pos[0] + 122, pos[1] + 224))
    return [pos_r, pos_g, pos_b]


def slider(screen, pos, color, text, myfont, i):
    slider_rect = [pos[0], pos[1], 255, 20]
    dimenciones_btn = [pos[0] + i, pos[1] - 5, 10, 30]
    rectBorder(screen, color, slider_rect, 3)
    rectBorder(screen, c.white, dimenciones_btn, 3)
    text = myfont.render(text, True, c.black)
    screen.blit(text, (pos[0] - 62, pos[1] - 1))
    return dimenciones_btn, slider_rect


def addFig(screen, tipo, origen, color, index, bengcreated):
    c.drawings["figura" + str(index)] = UI.Figuras(
        screen,
        tipo,
        color,
        [origen[0], origen[1], 0, 0],
        index,
        bengcreated
    )


def entre(eje, pos, dimenciones):
    x = dimenciones[0]
    y = dimenciones[1]
    w = dimenciones[2]
    h = dimenciones[3]
    if eje == "x":
        if x < pos[0] < (x + w):
            return True
        else:
            return False
    else:
        if y < pos[1] < (y + h):
            return True
        else:
            return False


def isOnPress(pos, dimenciones):
    if entre("x", pos, dimenciones) and entre("y", pos, dimenciones):
        return True
    else:
        return False
