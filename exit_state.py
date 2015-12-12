import random
import json
import os

from pico2d import *

import game_framework
import title_state





name = "MainState"
background = None
player1 = None
player2 = None
ground = None
pl1hp = None
pl2hp = None

class pl1hp:
    def __init__(self):
        self.hp=250
        self.hpx=305
        self.image = load_image('pl1hp.png')
        self.image2 = load_image('hpg.png')
    def draw(self):
        self.image.clip_draw(0,0,self.hp,25,self.hpx,700)
        self.image2.draw(305,700,250,25)
    def update(self):
        if pl1.status==4:
            if pl2.status2==2:
                self.hpx+=5
                self.hp-=10
            elif pl2.status2==3:
                self.hpx+=7
                self.hp-=14
            elif pl2.status2==7:
                self.hpx+=8
                self.hp-=16

class pl2hp:
    def __init__(self):
        self.hpx2=685
        self.hp2=250
        self.image = load_image('pl1hp.png')
        self.image2 = load_image('hpg.png')
    def draw(self):
        self.image.clip_draw(0,0,self.hp2,25,self.hpx2,700)
        self.image2.draw(685,700,250,25)
    def update(self):
        if pl2.status2==4:
            if pl1.status==2:
                self.hpx2-=5
                self.hp2-=10
            if pl1.status==3:
                self.hpx2-=5
                self.hp2-=10
            if pl1.status==7:
                self.hpx2-=8
                self.hp2-=16

class background:
    def __init__(self):
        self.image = load_image('background.png')
        self.image2 = load_image('ko.png')


    def draw(self):
        self.image.draw(500,400)
        self.image2.draw(499,700)


class ground:
    def __init__(self):
        self.image = load_image('ground2.png')
        self.x=500
        self.y=100
        self.drawc=0
        self.bgsound = load_wav('bgm.wav')
        self.bgsound.set_volume(1)
        self.bgsound.repeat_play()
        self.z=0

    def get_bb(self):
        return self.x-300,self.y-5,self.x+300, self.y+1
    def draw_bb(self):
        if self.drawc==1:
            draw_rectangle(*self.get_bb())

    def draw(self):
        self.image.draw(self.x, self.y)


class player1:

    def __init__(self):
        self.x, self.y = 120, 150
        self.frame = 0
        self.status=0
        self.drawc=0
        self.punchc=0
        self.kickc=0
        self.dashc=0
        self.jumpc=0
        self.energyc=0
        self.stepc=0
        self.touchc=0
        self.win = load_image('win.png')
        self.dashsound = load_wav('step.wav')
        self.dashsound.set_volume(10)
        self.hitsound = load_music('hit.mp3')
        self.hitsound.set_volume(10)
        self.exsound = load_wav('par3.wav')
        self.exsound.set_volume(50)


    def get_bb(self):
        if self.status ==7 and self.frame>=8:
            return self.x-20, self.y-50, self.x+150, self.y+50
        else:
            return self.x-20, self.y-50, self.x+20, self.y+50
    def draw_bb(self):
        if self.drawc==1:
            draw_rectangle(*self.get_bb())

    def update(self):
        if self.status == 1:
            self.dash = load_image('dash.png')
            if pl1.x+30>=pl2.x2:
                self.x+=0
            else:
                self.x+=15
            if self.frame==3:
                self.status = 0
                self.frame =0
                self.dashc =0
                self.dashsound.play()
        if self.status == 2:
            self.punch = load_image('funching.png')
            if self.frame==6:
                self.status = 0
                self.frame = 0
                self.punchc = 0
        if self.status == 3:
            self.kick = load_image('kick.png')
            if self.frame==4:
                self.status = 0
                self.frame = 0
                self.kickc = 0
        if self.status == 4:
            self.touch = load_image('touch.png')
            self.x-=15
            self.touchc+=1
            if self.touchc>0:
                self.status=4
            if self.frame==2:
                self.status = 0
                self.frame = 0
                self.hitsound.play()
                self.touchc=0
        if self.status == 5:
            self.die=load_image('die.png')
            if self.frame>7:
                ground.z=1
        if self.status == 6:
            self.jump = load_image('jump.png')
            self.y+=30
            if self.frame==3:
                self.status = 0
                self.frame = 0
                self.jumpc = 0
                self.y=ground.y+50
                self.dashsound.play()
        if self.status == 7:
            self.energy = load_image('energy.png')
            if self.frame ==13:
                self.status = 0
                self.frame = 0
                self.energyc = 0
            if collide(pl1,pl2) and pl2.status2!=7 and pl1.frame>=8:
                pl2.touch2= load_image('touch2.png')
                pl2.status2=4
                pl2.frame2=0
                if pl1.frame>=12:
                    pl2.sound=load_music('hit.mp3')
                    pl2.sound.play()

        if self.status == 9:
            self.step = load_image('step.png')
            self.x-=20
            if self.frame == 3:
                self.dashsound.play()
                self.status = 0
                self.frame = 0
                self.stepc = 0
        elif self.status == 0:
            self.image = load_image('waiting.png')
            if self.frame==2:
                self.status=0
                self.frame=0



    def draw(self):
        if self.status==1:
            self.dash.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            self.frame+=1
            self.dashc+=1
        if self.status==2:
            self.punch.clip_draw(self.frame * 100, 0, 100, 100, self.x-3, self.y-5)
            self.frame+=1
            self.punchc+=1
        if self.status==3:
            self.kick.clip_draw(self.frame*100, 0, 100, 100, self.x-3, self.y-5)
            self.frame+=1
            self.kickc+=1
        if self.status==0:
            self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
            self.frame+=1
        if self.status==4:
            self.touch.clip_draw(self.frame * 100,0, 100, 100, self.x, self.y)
            self.frame+=1
            self.touchc+=1
        if self.status==5:
            self.die.clip_draw(self.frame*100,0,100,100,self.x,self.y)
            self.frame+=1
            delay(0.1)
        if self.status==6:
            self.jump.clip_draw((self.frame-1) * 100, 0, 100, 100, self.x, self.y)
            self.frame+=1
            self.jumpc+=1
        if self.status==7:
            self.energy.clip_draw(self.frame*200, 0, 200, 100, self.x+40, self.y+2)
            self.frame+=1
            self.energyc+=1
        if self.status==9:
            self.step.clip_draw(self.frame*100,0,100,100,self.x,self.y)
            self.frame+=1
            self.stepc+=1

class player2:

    def __init__(self):
        self.x2, self.y2 = 880, 150
        self.frame2 = 0
        self.status2=0
        self.drawc2=0
        self.dashc=0
        self.punchc=0
        self.kickc=0
        self.jumpc=0
        self.sjumpc=0
        self.stepc=0
        self.gomuc=0
        self.touchc=0
        self.dashsound = load_wav('step.wav')
        self.dashsound.set_volume(7)
        self.hitsound = load_music('hit.mp3')
        self.hitsound.set_volume(10)

    def get_bb(self):
        if self.status2==7 and self.frame2>=3 and self.frame2 <=5:
            return self.x2-120,self.y2-50,self.x2+20,self.y2+50
        elif self.status2==7 and self.frame2>5:
            return self.x2-200,self.y2-50,self.x2+20,self.y2+50
        else:
            return self.x2-20, self.y2-50, self.x2+20, self.y2+50
    def draw_bb(self):
        if self.drawc2==1:
            draw_rectangle(*self.get_bb())

    def update(self):
        if self.status2 == 1:
            self.dash2 = load_image('dash2.png')
            if pl2.x2-30<=pl1.x:
                pl2.x2-=0
            else:
                self.x2-=15
            if self.frame2==3:
                self.status2 = 0
                self.frame2 =0
                self.dashc=0
                self.dashsound.play()
        if self.status2 == 2:
            self.punch2 = load_image('funching2.png')
            if self.frame2==6:
                self.status2 = 0
                self.frame2 = 0
                self.punchc=0
        if self.status2 == 3:
            self.kick2 = load_image('kick2.png')
            if self.frame2==4:
                self.status2 = 0
                self.frame2 = 0
                self.kickc=0
        if self.status2 == 4:
            self.touch2 = load_image('touch2.png')
            self.x2+=15
            self.touchc+=1
            if self.touchc>0:
                self.status2=4
            if self.frame2==2:
                self.status2 = 0
                self.frame2 = 0
                self.hitsound.play()
                self.touchc=0
        if self.status2==5:
            self.die=load_image('dye.png')
            if self.frame2>7:
                ground.z=1
        if self.status2 == 6:
            self.jump2= load_image('jump2.png')
            self.y2+=30
            if self.frame2==3:
                self.status2 = 0
                self.frame2 = 0
                self.jumpc = 0
                self.y2=ground.y+50
                self.dashsound.play()
        if self.status2 == 7:
            self.gomu = load_image('gomuu.png')
            if self.frame2==10:
                self.status2=0
                self.frame2 =0
                self. gomuc = 0
            if collide(pl1,pl2) and pl1.status!=7 and pl2.frame2>=3:
                pl1.touch = load_image('touch.png')
                pl1.status=4
                pl1.frame=0
                if pl2.frame2>=7:
                    pl1.sound=load_music('hit.mp3')
                    pl1.sound.play()

        if self.status2 ==8:
            self.sjump2 = load_image('sjump.png')
            if self.frame2>3:
                self.y2-=15
            else:
                self.y2+=25
            if self.x2-15>pl1.x:
                self.x2-=15
            else:
                self.x2+=0
            if self.frame2==5:
                self.status2 = 0
                self.frame2=0
                self.sjumpc=0
                self.y2=ground.y+50
                self.dashsound.play()
        if self.status2 == 9:
            self.step = load_image('step2.png')
            self.x2+=20
            if self.frame2 ==3:
                self.dashsound.play()
                self.status2=0
                self.frame2=0
                self.stepc=0
        elif self.status2 == 0:
            self.image2 = load_image('waiting2.png')
            if self.frame2==2:
                self.status2=0
                self.frame2=0

    def draw(self):
        if self.status2==1:
            self.dash2.clip_draw((self.frame2-1) * 100, 0, 100, 100, self.x2, self.y2)
            self.frame2+=1
            self.dashc+=1
        if self.status2==2:
            self.punch2.clip_draw((self.frame2-1) * 100, 0, 100, 100, self.x2+3, self.y2-5)
            self.frame2+=1
            self.punchc+=1
        if self.status2==3:
            self.kick2.clip_draw((self.frame2-1) * 100, 0, 100, 100, self.x2+3, self.y2-5)
            self.frame2+=1
            self.kickc+=1
        if self.status2==0:
            self.image2.clip_draw(self.frame2 * 100, 0, 100, 100, self.x2, self.y2)
            self.frame2+=1
        if self.status2==4:
            self.touch2.clip_draw(self.frame2 * 100,0, 100, 100, self.x2, self.y2)
            self.frame2+=1
            self.touchc+=1

        if self.status2==5:
            self.die.clip_draw(self.frame2*100,0,100,100,self.x2,self.y2)
            self.frame2+=1
            delay(0.1)

        if self.status2==6:
            self.jump2.clip_draw((self.frame2-1)*100,0,100,100,self.x2,self.y2)
            self.frame2+=1
            self.jumpc+=1
        if self.status2==7:
            self.gomu.clip_draw(self.frame2*300,0,300,100,self.x2-120,self.y2)
            self.frame2+=1
            self.gomuc+=1
        if self.status2==8:
            self.sjump2.clip_draw((self.frame2-1)*100,0,100,100,self.x2,self.y2)
            self.frame2+=1
            self.sjumpc+=1
        if self.status2==9:
            self.step.clip_draw(self.frame2*100,0,100,100,self.x2,self.y2)
            self.frame2+=1
            self.stepc+=1

def enter():
    global pl1,pl2, ground,bag,hp1,hp2
    bag=background()
    hp1=pl1hp()
    hp2=pl2hp()
    pl1 = player1()
    pl2 = player2()
    ground = ground()
    hide_lattice()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b : return False
    if right_a < left_b : return False
    if top_a < bottom_b : return False
    if bottom_a > top_b : return False

    return True

def exit():
    global pl1,pl2,ground,bag,hp1,hp2
    del(hp1)
    del(hp2)
    del(bag)
    del(pl2)
    del(pl1)
    del(ground)


def pause():
    pass

def resume():
    pass


def handle_events():
    global pl1,pl2
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        if event.type == SDL_KEYDOWN and event.key == SDLK_c and pl1.status!=5:
            pl1.drawc+=1
            pl2.drawc2+=1
            ground.drawc+=1
        if event.type == SDL_KEYUP and event.key == SDLK_c and pl1.status!=5:
            pl1.drawc-=1
            pl2.drawc2-=1
            ground.drawc-=1
        if event.type == SDL_KEYDOWN and event.key == SDLK_j and pl1.status!=5:
            if pl1.x+30>=pl2.x2:
                pl1.x+=0
            else:
                pl1.x+=7
        elif event.type == SDL_KEYDOWN and event.key == SDLK_g and pl1.status!=5:
            pl1.x-=7
        elif event.type == SDL_KEYDOWN and event.key == SDLK_d and pl1.punchc==0 and pl1. kickc==0 and pl1.status!=5 and pl1.jumpc==0 and pl1.energyc==0 and pl1.stepc==0 and pl1.touchc==0:
            pl1.status=1
            if pl1.dashc==1:
                pl1.frame=0
            if pl1.frame<=3 and pl1.dashc>0:
                pl1.status=1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a and pl1.kickc ==0 and pl1.dashc==0 and pl1.status!=5 and pl1.jumpc==0 and pl1.energyc==0 and pl1.stepc==0 and pl1.touchc==0:
            if collide(pl1,pl2):
                pl2.status2=4
                pl2.frame2=0
                pl1.status=2
                if pl1.punchc==1:
                    pl1.frame=0
                if pl1.frame<=6:
                    pl1.status=2
            else:
                pl1.status=2
                if pl1.punchc==1:
                    pl1.frame=0
                if pl1.frame<=6 and pl1.punchc>0:
                    pl1.status=2
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s and pl1.dashc==0 and pl1.punchc==0 and pl1.status!=5 and pl1.jumpc==0 and pl1.energyc==0 and pl1.stepc==0 and pl1.touchc==0:
            if collide(pl1,pl2):
                pl2.status2=4
                pl2.frame2=0
                pl1.status=3
                if pl1.kickc==1:
                    pl1.frame=0
                if pl1.frame<=4:
                    pl1.status=3
            else:
                pl1.status=3
                if pl1.kickc==1:
                    pl1.frame=0
                if pl1.kickc>0:
                    pl1.status=3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_y and pl1.dashc==0 and pl1.punchc==0 and pl1.status!=5 and pl1.kickc==0 and pl1.energyc==0 and pl1.stepc==0 and pl1.touchc==0:
            pl1.status=6
            if pl1.jumpc==1:
                pl1.frame=0
            if pl1.jumpc>0:
                pl1.status=6
        elif event.type == SDL_KEYDOWN and event.key ==SDLK_w and pl1.dashc==0 and pl1.punchc==0 and pl1.status!=5 and pl1.kickc==0 and pl1.jumpc==0 and pl1.stepc==0 and pl1.touchc==0:
            pl1.exsound.play()
            pl1.status=7
            if pl1.energyc==1:
                pl1.frme=0
            if pl1.energyc>0:
                pl1.status=7
        elif event.type == SDL_KEYDOWN and event.key ==SDLK_q and pl1.dashc==0 and pl1.punchc==0 and pl1.status!=5 and pl1.kickc==0 and pl1.jumpc==0 and pl1.energyc==0 and pl1.touchc==0:
            pl1.status=9
            if pl1.stepc==1:
                pl1.frame=0
            if pl1.stepc>0:
                pl1.status=9
        elif hp1.hp<0 or pl1.x<70:
            pl1.status=5

        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            pl2.x2+=7
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            if pl2.x2-30<=pl1.x:
                pl2.x2-=0
            else:
                pl2.x2-=7
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b and pl2.punchc==0 and pl2. kickc==0 and pl2.jumpc==0 and pl2.sjumpc==0 and pl2.stepc==0 and pl2.gomuc==0 and pl2.touchc==0:
            pl2.status2=1
            if pl2.dashc==1:
                pl2.frame2=0
            if pl2.frame2<=3 and pl2.dashc>0:
                pl2.status2=1

        elif event.type == SDL_KEYDOWN and event.key == SDLK_n and pl2.dashc==0  and pl2.kickc==0 and pl2.jumpc==0 and pl2.sjumpc==0 and pl2.stepc==0 and pl2.gomuc==0 and pl2.touchc==0:
            if collide(pl1,pl2):
                pl1.status=4
                pl1.frame=0
                pl2.status2=2
                if pl2.punchc==1:
                    pl2.frame2=0
                if pl2.frame2<6:
                    pl2.status2=2
            else:
                pl2.status2=2
                if pl2.punchc==1:
                    pl2.frame2=0
                if pl2.frame2<6 and pl2.punchc>0:
                    pl2.status2=2

        elif event.type == SDL_KEYDOWN and event.key == SDLK_m and pl2.dashc==0 and pl2.punchc==0 and pl2.jumpc==0 and pl2.sjumpc==0 and pl2.stepc==0 and pl2.gomuc==0 and pl2.touchc==0:
            if collide(pl1,pl2):
                pl1.status=4
                pl1.frame=0
                pl2.status2=3
                if pl2.kickc==1:
                    pl2.frame2=0
                if pl2.frame2<=4:
                    pl2.status2=3
            else:
                pl2.status2=3
                if pl2.kickc==1:
                    pl2.frame2=0
                if pl2.kickc>0:
                    pl2.status2=3
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP and pl2.dashc==0 and pl2.punchc==0 and pl2.kickc==0 and pl2.sjumpc==0 and pl2.stepc==0 and pl2.gomuc==0 and pl2.touchc==0:
            pl2.status2=6
            if pl2.jumpc==1:
                pl2.frame2=0
            if pl2.jumpc>0:
                pl2.status2=6
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l and pl2.dashc==0 and pl2.punchc==0 and pl2.kickc==0 and pl2.sjumpc==0 and pl2.stepc==0 and pl2.jumpc==0  and pl2.touchc==0:
            pl2.status2=7
            if pl2.gomuc==1:
                pl2.frame2=0
            if pl2.gomuc>0:
                pl2.status2=7

        elif event.type == SDL_KEYDOWN and event.key == SDLK_k and pl2.dashc==0 and pl2.punchc==0 and pl2.kickc==0 and pl2.jumpc==0 and pl2.stepc==0 and pl2.gomuc==0  and pl2.touchc==0:
            pl2.status2=8
            if pl2.sjumpc==1:
                pl2.frame2=0
            if pl2.sjumpc>0:
                pl2.status2=8
        elif event.type == SDL_KEYDOWN and event.key == SDLK_v and pl2.dashc==0 and pl2.punchc==0 and pl2.kickc==0 and pl2.jumpc==0 and pl2.sjumpc==0 and pl2.gomuc==0 and pl2.touchc==0:
            pl2.status2=9
            if pl2.stepc==1:
                pl2.frame2=0
            if pl2.stepc>0:
                pl2.status2=9
        elif hp2.hp2<0 or pl2.x2>910:
            pl2.status2=5



def update():

        pl1.update()
        pl2.update()
        hp1.update()
        hp2.update()
        delay(0.05)




def draw():

    clear_canvas()
    if ground.z==0:
        bag.draw()
        hp1.draw()
        hp2.draw()
        ground.draw()
        pl1.draw_bb()
        pl2.draw_bb()
        ground.draw_bb()
        pl1.draw()
        pl2.draw()
    else:
        clear_canvas()




    update_canvas()








