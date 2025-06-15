import pygame as pg 
import game
class Obstacles(pg.sprite.Sprite) :
    image = pg.image.load("../sprites/Obstacles/obstacle.png")
    # imsc = pg.transform.smoothscale_by(image,(0.3,0.3))
    imsc = image
    price = 200
    def __init__(self,groups,pos):
        super().__init__(groups)
        self.image = Obstacles.imsc
        self.rect = self.image.get_frect(center=pos)
        self.health = 100
        self.hitbox = self.rect.inflate(-200,-200)
        self.hitbox.top += 10
        self.health = 40
        self.obst = True
    def kill_obst (self):
        # broke_sound.play()       when sound is loaded 
        self.kill()
    def obst_health_dec(self,damage):
        self.health -= damage
        if self.health <= 0:           
            self.kill_obst()

def put_obst(all_spr,Obst_spr,stack): 
        if pg.mouse.get_just_pressed()[2] and  game.gold_quantity >Obstacles.price:
            game.gold_quantity -= Obstacles.price 
            mouse_pos = pg.mouse.get_pos()
            world_pos = pg.Vector2(mouse_pos) - all_spr.offset
            stack.push(Obstacles((all_spr, Obst_spr),world_pos))

def check_undo(stack):
        if pg.key.get_just_pressed()[pg.K_z]:
            stack.pop()
            game.gold_quantity += 200


    