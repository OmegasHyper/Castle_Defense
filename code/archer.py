import os
from Queue import Queue
from PiriorityQueue import PriorityQueue
import pygame as pg
from arrow import Arrow
from settings import *
from enemy import *

class Archer(pg.sprite.Sprite) :
    def __init__(self,groups,pos, round, direction = "NT"):
        super().__init__(groups)
        self.round = round
        self.frames = None  # Store animations for each direction
        self.isArcher = True  # Exclude archers from y-sorting
        self.all_sprites = groups[0]
        self.pos = pos
        self.direction = direction
        self.attack_range = 500
        self.load_images()

        self.current_frame = 1
        self.animation_speed = 50
        self.last_update = pg.time.get_ticks()
        self.arching = False

        self.image = self.frames[self.direction][0]  # Static image
        self.rect = self.image.get_rect(center=self.pos)


        self.enemy_queue = Queue()


        self.current_target = None

    def load_images(self):
        self.frames = {'ET': [], 'NT': [], 'ST': [], 'WT': []}
        base_path = "../sprites/archers"
        for dir_name in self.frames.keys():
            path = os.path.join(base_path, dir_name)
            for folder_path, sub_folder, file_names in os.walk(path):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = os.path.join(folder_path, file_name)
                        surf = pg.image.load(full_path).convert_alpha()
                        self.frames[dir_name].append(surf)

    def can_shoot(self, shoot_direction):

        if self.direction == "NT" and shoot_direction.y > 0:
            return False
        if self.direction == "ET" and shoot_direction.x < 0:
            return False
        if self.direction == "ST" and shoot_direction.y < 0:
            return False
        if self.direction == "WT" and shoot_direction.x > 0:
            return False
        return True

    def update_archer(self, dt, enemy_group):

        enemies_in_queue = set()
        temp_queue = Queue()
        while not self.enemy_queue.isempty():
            e = self.enemy_queue.dequeue()
            enemies_in_queue.add(e)
            temp_queue.enqueue(e)
        self.enemy_queue = temp_queue


        for enemy in enemy_group:
            if hasattr(enemy, "rect"):
                distance = pg.math.Vector2(self.rect.center).distance_to(enemy.rect.center)
                if distance <= self.attack_range:
                    shoot_direction = pg.Vector2(enemy.rect.center) - pg.Vector2(self.rect.center)
                    if self.can_shoot(shoot_direction):
                        if enemy not in enemies_in_queue:
                            # New enemy enters range - enqueue
                            self.enemy_queue.enqueue(enemy)
                            enemies_in_queue.add(enemy)


        temp_queue = Queue()
        while not self.enemy_queue.isempty():
            e = self.enemy_queue.dequeue()
            # still alive
            if hasattr(e, "health") and e.health > 0:
                dist = pg.math.Vector2(self.rect.center).distance_to(e.rect.center)
                if dist <= self.attack_range:
                    shoot_dir = pg.Vector2(e.rect.center) - pg.Vector2(self.rect.center)
                    if self.can_shoot(shoot_dir):
                        temp_queue.enqueue(e)
                    else:
                        # Not facing, discard
                        if self.current_target == e:
                            self.current_target = None
                else:
                    # Out of range
                    if self.current_target == e:
                        self.current_target = None
            else:
                # Dead enemy
                if self.current_target == e:
                    self.current_target = None
        self.enemy_queue = temp_queue

        if self.enemy_queue.isempty():

            self.arching = False
            self.current_target = None
            self.image = self.frames[self.direction][0]
            self.current_frame = 1
            return


        priority_queue = PriorityQueue()
        temp_queue = Queue()

        while not self.enemy_queue.isempty():
            e = self.enemy_queue.dequeue()
            priority_queue.enqueue(e, e.piriority)
            temp_queue.enqueue(e)


        self.enemy_queue = temp_queue

        high_priority_enemy = None
        low_priority_enemy = None


        if not priority_queue.high.isempty():
            high_priority_enemy = priority_queue.high.get_front()
        if not priority_queue.low.isempty():
            low_priority_enemy = priority_queue.low.get_front()

        if self.current_target is not None:
            # Check if current_target still valid and priority
            def in_priority_queue(enemy, pq):

                in_high = False
                in_low = False

                temp_h = Queue()
                found = False
                while not pq.high.isempty():
                    item = pq.high.dequeue()
                    temp_h.enqueue(item)
                    if item == enemy:
                        found = True
                while not temp_h.isempty():
                    pq.high.enqueue(temp_h.dequeue())
                if found:
                    return True

                temp_l = Queue()
                found = False
                while not pq.low.isempty():
                    item = pq.low.dequeue()
                    temp_l.enqueue(item)
                    if item == enemy:
                        found = True
                while not temp_l.isempty():
                    pq.low.enqueue(temp_l.dequeue())
                return found

            if not in_priority_queue(self.current_target, priority_queue):

                self.current_target = None


        if self.current_target is None:
            if high_priority_enemy is not None:
                self.current_target = high_priority_enemy
            else:
                self.current_target = low_priority_enemy

        else:

            is_current_high = False
            if self.current_target == high_priority_enemy:
                is_current_high = True
            if not is_current_high and high_priority_enemy is not None:

                self.current_target = high_priority_enemy


        if self.current_target is None:
            self.arching = False
            self.image = self.frames[self.direction][0]
            self.current_frame = 1
            return

        self.arching = True
        now = pg.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame - 1 + 1) % (len(self.frames[self.direction]) - 1) + 1
            self.image = self.frames[self.direction][self.current_frame]

            if self.current_frame == 6:
                # Shoot arrow at current target
                Arrow(self.all_sprites, self.rect, self.current_target, self.direction)

    def draw_range(self, surface):
        screen_pos = pg.Vector2(self.rect.center)

        range_surface = pg.Surface((self.attack_range * 2, self.attack_range * 2), pg.SRCALPHA)
        arc_rect = pg.Rect(0, 0, self.attack_range * 2, self.attack_range * 2)
        direction_angle = {
            'NT': (0.4, 2.74),
            'ST': (3.54, 5.88),
            'ET': (5.1, 1.17),
            'WT': (1.97, 4.31)
        }

        start_angle, end_angle = direction_angle.get(self.direction, (0, 6.28))

        surface.blit(range_surface, (screen_pos.x - self.attack_range, screen_pos.y - self.attack_range))
        surface.blit(self.image, self.rect.topleft)

