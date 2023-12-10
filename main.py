import pygame as pg
import numpy  as np
import modelPh

buttons = pg.sprite.Group()

class Button(pg.sprite.Sprite):
    ''' Create a button clickable with changing hover color'''
    def __init__(self, text="Click",
                pos=(0,0), fontsize=16,
                colors="white on blue", hover_colors="red on green",
                command=lambda: print("No command activated for this button")):
        super().__init__()
        self.text = text
        self.command = command
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.fgh, self.bgh = hover_colors.split(" on ")
        self.font = pg.font.SysFont("Arial", fontsize)
        self.pos = pos
        self.create_original()
        self.create_hover_image()
    def create_original(self):
        self.image = self.create_bg(self.text, self.fg, self.bg)
        self.original_image = self.image.copy()
    def create_hover_image(self):
        self.hover_image = self.create_bg(self.text, self.fgh, self.bgh)
        self.pressed = 1
        buttons.add(self)
    def create_bg(self, text, fg, bg):
        self.text = text
        image = self.font.render(self.text, 1, fg)
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = self.pos
        bgo = pg.Surface((self.rect.w, self.rect.h))
        bgo.fill(bg)
        bgo.blit(image, (0,0))
        return bgo
    def update(self):
        ''' CHECK IF HOVER AND IF CLICK THE BUTTON '''
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.hover_image
            self.check_if_click()
        else:
            self.image = self.original_image
    def check_if_click(self):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0] and self.pressed == 1:
                # print("Execunting code for button '" + self.text + "'")
                self.command()
                self.pressed = 0
            if pg.mouse.get_pressed() == (0,0,0):
                self.pressed = 1


def draw_line_dashed(surface, color, start_pos, end_pos, width = 1, dash_length = 10, exclude_corners = True):

    # convert tuples to numpy arrays
    start_pos = np.array(start_pos)
    end_pos   = np.array(end_pos)

    # get euclidian distance between start_pos and end_pos
    length = np.linalg.norm(end_pos - start_pos)

    # get amount of pieces that line will be split up in (half of it are amount of dashes)
    dash_amount = int(length / dash_length)

    # x-y-value-pairs of where dashes start (and on next, will end)
    dash_knots = np.array([np.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()

    return [pg.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)
            for n in range(int(exclude_corners), dash_amount - int(exclude_corners), 2)]




pg.init()

WIDTH, HEIGHT = 800, 700
FPS = 60

blue = (0,0,255)
green = (0,255,0)
font = pg.font.Font(None, 32)
font2 = pg.font.Font(None, 20)

window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Modeling')
window.fill(pg.Color('white'))
clock = pg.time.Clock()

def drawBase(col = pg.Color('white')):
    window.fill(col)
    draw_line_dashed(window, pg.Color('black'), (100,200), (500,200),1)
    pg.draw.ellipse(window, pg.Color('black'), (60, 200, 80, 200),2)
    pg.draw.ellipse(window, pg.Color('black'), (460, 200, 80, 200),2)
    draw_line_dashed(window, pg.Color('black'), (100,400), (500,400),1)


    pg.draw.line(window, pg.Color('black'), (100,100), (500,100),1)
    pg.draw.ellipse(window, pg.Color('black'), (50, 100, 100, 400),2)
    pg.draw.ellipse(window, pg.Color('black'), (450, 100, 100, 400),2)
    pg.draw.line(window, pg.Color('black'), (100,500), (500,500),1)

    buttons.draw(window)


drawBase()
el = pg.draw.circle(window,pg.Color('blue'),(100,150),5 )

input_box = pg.Rect(600, 100, 100, 32)
color_inactive = pg.Color('lightskyblue3')
color_active = pg.Color('dodgerblue2')
color = color_inactive
active = False
text = 'U = '
done = False
Model = modelPh.MyClass()
Uans = font2.render('Минимальное U при котором электрон не вылетает из конденсатора: ' + str(Model.U_ans), True,  pg.Color('black'))
window.blit(Uans, (100,550))

u = 11.276479840278625

textT = ''
textV = ''

window.blit(font.render(textT, True,  pg.Color('black')), (600,200))
window.blit(font.render(textV, True,  pg.Color('black')), (600,250))



def model():
    posY = 150
    posx = 100
    lW = 400
    hW = 50
    Model.U = u
    flag = Model.DO()
    x = Model.x_
    y = Model.y_
    drawBase()
    pg.draw.circle(window,pg.Color('blue'),(posx, posY),5)
    textT = f'{Model.t_ans:.2f}' + ' сек'
    textT = str(Model.t_ans)
    point = textT.find('.')
    textT = textT[:point+3]+ ' сек'
    textV = f'{Model.v_ans:.2f}' + ' м/с'

    
    txt_graf = font.render("Графики", True,  pg.Color('black'))
    rec = pg.draw.rect(window,  pg.Color('green'), (600,300, 130 ,40))
    window.blit(txt_graf, (605, 305))
    for i in range (0, Model.toch):
        drawBase()

        pg.draw.circle(window,pg.Color('blue'),(posx+x[i]*lW/Model.l, posY  + hW -  2*y[i]*hW/Model.d),5)
        if (y[i] == 0):
            break
        
        txt_surface = font.render(text, True, pg.Color('red'))
        # Resize the box if the text is too long.
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(window, color, input_box, 2)

        Uans = font2.render('Минимальное U при котором электрон не вылетает из конденсатора: ' + str(Model.U_ans), True,  pg.Color('black'))
        window.blit(Uans, (50,550)) 

        window.blit(font.render(textT, True,  pg.Color('black')), (600,200))
        window.blit(font.render(textV, True,  pg.Color('black')), (600,250))

        pg.draw.rect(window,  pg.Color('green'), (600,300, 130 ,40))
        window.blit(txt_graf, (605, 305))

        pg.display.update()

    col = (pg.Color(255, 105, 105))
    if flag :
        col = pg.Color(193, 242, 176)
  
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if rec.collidepoint(event.pos):
                    # Toggle the active variable.
                    Model.GetGrap()
                    break
        
        drawBase(col)

        txt_surface = font.render(text, True, pg.Color('red'))
        # Resize the box if the text is too long.
        width = max(100, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(window, color, input_box, 2)

        Uans = font2.render('Минимальное U при котором электрон не вылетает из конденсатора: ' + str(Model.U_ans), True,  pg.Color('black'))
        window.blit(Uans, (50,550)) 

        window.blit(font.render(textT, True,  pg.Color('black')), (600,200))
        window.blit(font.render(textV, True,  pg.Color('black')), (600,250))


        pg.draw.rect(window,  pg.Color('green'), (600,300, 130 ,40))
        window.blit(txt_graf, (605, 305))


        pg.display.update()

b1 = Button("RUN", pos=(350,40),
            fontsize=30,
            colors="black on green",
            hover_colors="black on red",
            command=lambda: model())



while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
        if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        color = color_active
                        try:
                            u = text.find("U = ")
                            u = text[(u+4) :]
                            u = int(u)
                            print(u)
                        except:
                            text = 'U = '
                        
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
    drawBase()
    txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
    width = max(100, txt_surface.get_width()+10)
    input_box.w = width
        # Blit the text.
    window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
    pg.draw.rect(window, color, input_box, 2)

    pg.draw.rect(window,  pg.Color('green'), (350, 40, 65,33))
    txt_surface = font.render("RUN", True,  pg.Color('black'))
        # Resize the box if the text is too long.
        # Blit the text.
    window.blit(txt_surface, (355, 45))

    Uans = font2.render('Минимальное U при котором электрон не вылетает из конденсатора: ' + str(Model.U_ans), True,  pg.Color('black'))
    window.blit(Uans, (50,550))   

    window.blit(font.render(textT, True,  pg.Color('black')), (600,200))
    window.blit(font.render(textV, True,  pg.Color('black')), (600,250))

    buttons.update()
    buttons.draw(window)
    pg.display.update()
    clock.tick(FPS)

pg.quit()

