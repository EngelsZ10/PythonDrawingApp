import pygame
from Modulos import constantes as c
import Modulos.funciones as f


class Boton:
    def __init__(self, color, dimenciones, screen, size=30, text_color=c.black, texto="", image=""):
        self.dimenciones = dimenciones
        self.color = color
        self.image = image
        self.screen = screen
        self.texto = texto
        self.font = pygame.font.SysFont("rubik mono one", size)
        self.text = self.font.render(texto, True, text_color)

    def onPress(self, pos):
        return f.isOnPress(pos, self.dimenciones)

    def posCenter(self):
        pos_x = self.dimenciones[2] - self.text.get_width()
        pos_y = self.dimenciones[3] - self.text.get_height()
        pos = int(self.dimenciones[0] + pos_x / 2), int(self.dimenciones[1] + pos_y / 2)
        return pos

    def build_cont(self, ):
        pygame.draw.rect(self.screen, self.color, self.dimenciones, 0)
        if self.image == "":
            self.screen.blit(self.text, self.posCenter())
        else:
            pass

    def build(self):
        pygame.draw.rect(self.screen, self.color, self.dimenciones)
        self.build_cont()


class Figuras:
    def __init__(self, screen, tipo, color, dimenciones, index, start, grosor=0):
        self.tipo = tipo
        self.color = color
        self.dimenciones = dimenciones
        self.grosor = grosor
        self.index = index
        self.start = start
        self.screen = screen
        self.esquina = "inf-der"
        self.selected = False
        self.esquinas = ["sup-izq", "sup-der", "inf-izq", "inf-der"]

    def tri(self):
        if self.esquina[0:3] == "inf":
            return [
                (self.dimenciones[0],
                 self.dimenciones[1]),
                (self.dimenciones[0] + self.dimenciones[2],
                 self.dimenciones[1]),
                (self.dimenciones[0] + self.dimenciones[2]/2,
                 self.dimenciones[1] + self.dimenciones[3])
            ]
        else:
            return [
                (self.dimenciones[2] / 2 + self.dimenciones[0],
                 self.dimenciones[1]),
                (self.dimenciones[0],
                 self.dimenciones[1] + self.dimenciones[3]),
                (self.dimenciones[0] + self.dimenciones[2],
                 self.dimenciones[1] + self.dimenciones[3])
            ]

    def linea(self):
        # y = self.dimenciones[1] + self.dimenciones[3]/2
        if self.esquina == "sup-der":
            return [
                (self.dimenciones[0],
                 self.dimenciones[1] + self.dimenciones[3]),
                (self.dimenciones[0] + self.dimenciones[2],
                 self.dimenciones[1])
            ]
        elif self.esquina == "inf-izq":
            return [
                (self.dimenciones[0] + self.dimenciones[2],
                 self.dimenciones[1]),
                (self.dimenciones[0],
                 self.dimenciones[1] + self.dimenciones[3])
            ]
        else:
            return [
                (self.dimenciones[0],
                 self.dimenciones[1]),
                (self.dimenciones[0] + self.dimenciones[2],
                 self.dimenciones[1] + self.dimenciones[3])
            ]

    def dibuja(self, screen, is_selected):
        if self.tipo == "Rectangulo":
            pygame.draw.rect(screen, self.color, self.dimenciones, self.grosor)
        elif self.tipo == "Circulo":
            pygame.draw.ellipse(screen, self.color, self.dimenciones, self.grosor)
        elif self.tipo == "Triangulo":
            trian = self.tri()
            pygame.draw.polygon(self.screen, self.color, trian, self.grosor)
        elif self.tipo == "Linea":
            Linea = self.linea()
            pygame.draw.line(self.screen, self.color, Linea[0], Linea[1], self.grosor + 3)
        if is_selected:
            self.isSelect()

    def move(self, rel):
        self.dimenciones = [
            self.dimenciones[0] + rel[0],
            self.dimenciones[1] + rel[1],
            self.dimenciones[2],
            self.dimenciones[3]
        ]

    def cuadros_pos(self, cuadro, n):
        if cuadro == "sup-izq":
            if self.start:
                self.esquina = "sup-izq"
            return (
                self.dimenciones[0] - n / 2,
                self.dimenciones[1] - n / 2,
                n, n
            )
        elif cuadro == "sup-der":
            if self.start:
                self.esquina = "sup-der"
            return (
                self.dimenciones[0] + self.dimenciones[2] - n / 2,
                self.dimenciones[1] - n / 2,
                n, n
            )
        elif cuadro == "inf-izq":
            if self.start:
                self.esquina = "inf-izq"
            return (
                self.dimenciones[0] - n / 2,
                self.dimenciones[1] + self.dimenciones[3] - n / 2,
                n, n
            )
        else:
            if self.start:
                self.esquina = "inf-der"
            return (
                (self.dimenciones[0] + self.dimenciones[2]) - n / 2,
                (self.dimenciones[1] + self.dimenciones[3]) - n / 2,
                n, n
            )

    def isSelect(self):
        pygame.draw.rect(self.screen, c.black, self.dimenciones, 1)
        for i in self.esquinas:
            pygame.draw.rect(self.screen, c.white, self.cuadros_pos(i, 8))
            pygame.draw.rect(self.screen, c.black, self.cuadros_pos(i, 8), 1)

    def size(self, origen, mouse_pos):
        if origen[0] < mouse_pos[0] and origen[1] < mouse_pos[1]:
            self.dimenciones = [
                origen[0],
                origen[1],
                mouse_pos[0] - origen[0],
                mouse_pos[1] - origen[1]
            ]
        elif origen[0] > mouse_pos[0] and origen[1] > mouse_pos[1]:
            self.dimenciones = [
                mouse_pos[0],
                mouse_pos[1],
                origen[0] - mouse_pos[0],
                origen[1] - mouse_pos[1]
            ]
        elif origen[0] > mouse_pos[0] and origen[1] < mouse_pos[1]:
            self.dimenciones = [
                mouse_pos[0],
                origen[1],
                origen[0] - mouse_pos[0],
                mouse_pos[1] - origen[1]
            ]
        else:
            self.dimenciones = [
                origen[0],
                mouse_pos[1],
                mouse_pos[0] - origen[0],
                origen[1] - mouse_pos[1]
            ]
        self.isCuadroPress(mouse_pos)
        """    
        if self.tipo == "linea":
            self.dimenciones[3] = self.grosor + 11
            self.dimenciones[1] = origen[1]
        """

    def cuadroContrario(self, cuadro):
        if cuadro == "sup-izq":
            return self.cuadros_pos("inf-der", 0)
        elif cuadro == "sup-der":
            return self.cuadros_pos("inf-izq", 0)
        elif cuadro == "inf-izq":
            return self.cuadros_pos("sup-der", 0)
        elif cuadro == "inf-der":
            return self.cuadros_pos("sup-izq", 0)

    def isCuadroPress(self, pos):
        if self.tipo == "Linea":
            pass
        for i in self.esquinas:
            if f.isOnPress(pos, self.cuadros_pos(i, 8)):
                return [True, i]
        return [False, None]

    def onPress(self, pos):
        return f.isOnPress(pos, self.dimenciones)
