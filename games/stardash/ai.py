# This is where you build your AI for the Stardash game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
import math
from collections import namedtuple
import datetime
# <<-- /Creer-Merge: imports -->>

P = namedtuple('P', ['x', 'y'])

class AI(BaseAI):
    """ The AI you add and improve code inside to play Stardash. """

    @property
    def game(self):
        """The reference to the Game instance this AI is playing.

        :rtype: games.stardash.game.Game
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self):
        """The reference to the Player this AI controls in the Game.

        :rtype: games.stardash.player.Player
        """
        return self._player # don't directly touch this "private" variable pls

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
            player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "KHAN!!!!!!!" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self):
        """ This is called once the game starts and your AI knows its player and
            game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
            dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won
            or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        if self.game.current_turn < 2:
            print('STARDATE %s' % datetime.datetime.now())
        print('Turn %s' % self.game.current_turn)

        unmined_mythicite = sum(b.amount for b in self.game.bodies if b.material_type == 'mythicite')
        carried_mythicite = sum(u.mythicite for u in self.player.units)
        enemy_carried_mythicite = sum(u.mythicite for u in self.player.opponent.units)
        can_win_by_running_away = self.player.victory_points > (self.player.opponent.victory_points + unmined_mythicite + enemy_carried_mythicite)
        my_soldiers = sum(1 for u in self.player.units if u.job.title in ['missileboat', 'corvette'])
        enemy_soldiers = sum(1 for u in self.player.opponent.units if u.job.title in ['missileboat', 'corvette'])
        military_disadvantage = (enemy_soldiers > (3 * my_soldiers + 5))
        must_win_by_running_away = can_win_by_running_away and military_disadvantage
        must_win_by_combat = (self.player.victory_points + unmined_mythicite + carried_mythicite) < (self.player.opponent.victory_points)
        need_missileboat = must_win_by_combat or can_win_by_running_away
        asteroids_left = sum(1 for b in self.game.bodies if b.material_type != 'none')
        need_miner = sum(1 for u in self.player.units if u.job.title == 'miner') < asteroids_left
        money_buffer = 80 if (enemy_soldiers or can_win_by_running_away or must_win_by_combat or military_disadvantage or self.game.current_turn > 15) else 0

        toward_center = 1 if self.player.home_base.x < self.game.size_x / 2 else -1
        x = self.player.home_base.x + toward_center*(self.player.home_base.radius-1)
        y = self.player.home_base.y
        miner = next(j for j in self.game.jobs if j.title == 'miner')
        missileboat = next(j for j in self.game.jobs if j.title == 'missileboat')

        # This is stupid, but works
        if 5 < self.game.current_turn < 20 and self.player.home_base.x < self.game.size_x / 2:
            need_missileboat = True
            need_miner = True
        if 15 < self.game.current_turn < 30 and self.player.home_base.x > self.game.size_x / 2:
            need_missileboat = True
            need_miner = False
        if 35 < self.game.current_turn < 50 and self.player.home_base.x < self.game.size_x / 2:
            need_missileboat = True
            need_miner = False
        if 55 < self.game.current_turn < 70 and self.player.home_base.x > self.game.size_x / 2:
            need_missileboat = True
            need_miner = False

        #can_win_by_running_away = False
        #must_win_by_combat = False
        if need_miner and need_missileboat:
            while self.player.money >= miner.unit_cost + money_buffer:
                print('Spawn!')
                # TODO: Spawn at edge
                self.player.home_base.spawn(x, y, "miner")
                if self.player.money >= missileboat.unit_cost + money_buffer:
                    self.player.home_base.spawn(x, y, "missileboat")
        if must_win_by_running_away:
            print('Must win by running away!')
            self.run_away()
        if need_missileboat:
            while self.player.money >= missileboat.unit_cost + money_buffer:
                self.player.home_base.spawn(x, y, "missileboat")
        if need_miner:
            while self.player.money >= miner.unit_cost + money_buffer:
                print('Spawn!')
                # TODO: Spawn at edge
                self.player.home_base.spawn(x, y, "miner")
        self.escape_missiles()
        if can_win_by_running_away or must_win_by_combat:
            if must_win_by_combat:
                print('Must win by combat!')
            elif can_win_by_running_away:
                print('Fight anyway')
            self.kill_enemy()
            self.mine()
        else:
            print('Mine')
            self.mine()
            self.kill_enemy()
        if asteroids_left == 0:
            print('No more asteroids, hide')
            self.run_away()

        return True
        # <<-- /Creer-Merge: runTurn -->>

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here

    def escape_missiles(self):
        for p in self.game.projectiles:
            if p.owner != self.player:
                u = p.target
                #if True or u.job.title in ['miner', 'transport']:
                if dis(p, u) < self.game.projectile_speed * 3:
                    print('escape!')
                    target = self.player.home_base
                    #if dis(u, self.player.home_base) < self.player.home_base.radius:
                    if u.energy == u.job.energy:
                        target = P(target.x, away_y(self, p.y, 200))
                    move_toward(self, u, target, radius=1)
                    dash_toward(self, u, target, radius=1)

    def run_away(self):
        hiders = [u for u in self.player.units if u.job.title in ['miner', 'transport']]
        if not hiders:
            return
        if self.player.home_base.x < self.game.size_x / 2:
            _, _, furthest = min((u.x, int(u.id), u) for u in hiders)
        else:
            _, _, furthest = max((u.x, -int(u.id), u) for u in hiders)
        hiders = [furthest]
        for u in hiders:
            if u.job.title in ['miner', 'transport']:
                if u.energy < u.job.energy * 0.5:
                    move_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)
                    dash_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)
                else:
                    enemy_soldiers = [u for u in self.player.opponent.units if u.job.title in ['missileboat', 'corvette']]
                    if not enemy_soldiers:
                        break
                    enemy_centroid_y = sum(u.y for u in enemy_soldiers) / len(enemy_soldiers)
                    if enemy_centroid_y < self.game.size_y / 2:
                        goal_y = self.game.size_y - 1
                    else:
                        goal_y = 1
                    move_toward(self, u, P(self.player.home_base.x, goal_y), radius=1)
                    dash_toward(self, u, P(self.player.home_base.x, goal_y), radius=1)
                u.dash(u.x, u.y)  # Prevent movement

    def kill_enemy(self):
        marked = dict()
        for p in self.game.projectiles:
            if p.owner == self.player:
                marked[p.target] = p
        for u in self.player.units:
            if u.job.title in ['missileboat', 'corvette']:
                if u.energy < u.job.energy*0.1:
                    move_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)
                    #dash_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)
                else:
                    enemies = [e for e in self.player.opponent.units if e.energy and e not in marked]
                    if not enemies:
                        print('No enemies!')
                        continue
                    n, d = nearest(u, enemies)
                    if dis(u, n) < u.job.range:
                        print('Attack %s %s' % (u.id, u.attack(n)))
                        if u.job.title == 'missileboat':
                            marked[n] = 'aaaaaaaaaaaaaaaaa'
                    print('Toward attack %s %s' % (u.id, move_toward(self, u, n, radius=0)))
                    if dis(u, n) < u.job.range and not u.acted:
                        print('Attack %s %s' % (u.id, u.attack(n)))
                        if u.job.title == 'missileboat':
                            marked[n] = 'aaaaaaaaaaaaaaaaa'
                    if not u.acted:
                        print('dash %s %s' % (u.id, dash_toward(self, u, n, radius=0, maintain_energy=u.job.energy*0.5)))

    def mine(self):
        for u in self.player.units:
            if u.job.title == 'miner':
                materials = u.genarium + u.legendarium + u.mythicite + u.rarium
                if materials == u.job.carry_limit:
                    print('Move back %s %s' % (u.id, move_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)))
                    print('Dash back %s %s' % (u.id, dash_toward(self, u, self.player.home_base, radius=self.player.home_base.radius-1)))
                    # Planet will automatically grab materials
                else:
                    legendarium = filter_asteroids(self, [b for b in self.game.bodies if b.material_type == 'legendarium'])
                    rarium = filter_asteroids(self, [b for b in self.game.bodies if b.material_type == 'rarium'])
                    genarium = filter_asteroids(self, [b for b in self.game.bodies if b.material_type == 'genarium'])
                    mythicite = filter_asteroids(self, [b for b in self.game.bodies if b.material_type == 'mythicite'])
                    if self.game.current_turn < self.game.orbits_protected:
                        mythicite = list()
                    if self.player.victory_points > self.game.mythicite_amount / 2:
                        mythicite = list()
                    #if mythicite and len(self.player.units) > 9 and self.player.victory_points < self.player.opponent.victory_points + sum(b.amount for b in mythicite)):
                    if mythicite and len(self.player.units) > 9:
                        print('Gather mythicite')
                        target_bodies = mythicite or legendarium or rarium or genarium
                    else:
                        target_bodies = legendarium or rarium or mythicite or genarium
                    n, d = nearest(u, target_bodies)
                    if n:
                        next_pos = P(*predict_asteroid(self, n, 1))
                        print('toward? %s %s' % (u.id, move_toward(self, u, next_pos, radius=0)))
                        if dis(u, n) <= (u.job.range + n.radius):
                            print('mined? %s %s %s' % (u.id, u.mine(n), n.material_type))
                        else:
                            next_pos = P(*predict_asteroid(self, n, 2))
                            print('dash? %s %s' % (u.id, dash_toward(self, u, next_pos, radius=0)))
                    else:
                        print('no nearest!')

    def verify_predict(self):
        for body in self.game.bodies:
            if body.material_type != 'none':
                px, py = predict_asteroid(self, body, 2)
                print('allpos ', body.id, self.game.current_turn, body.x, body.y, px, py)

def filter_asteroids(ai, objs):
    left = ai.player.home_base.x < (ai.game.size_x / 2)
    filtered = list()
    for obj in objs:
        if (obj.x < ai.game.size_x / 2) != left:
            continue
        if ai.player.victory_points > ai.game.mythicite_amount / 2 and obj.owner:
            continue
        #if dis(ai.player.home_base, obj) > dis(ai.player.home_base, ai.game.bodies[2]):
        #    continue
        if obj.amount < 1:
            continue
        filtered.append(obj)
    return filtered

def nearest_asteroid(ai, center, objs):
    nearest_d = 99999999999999999999
    nearest_obj = None
    for obj in objs:
        if not obj.amount:
            continue
        predicted = P(*predict_asteroid(ai, obj, turns=2))
        d = dis(center, predicted)
        if d < nearest_d:
            nearest_d = d
            nearest_obj = obj
    return nearest_obj, nearest_d

def predict_asteroid(ai, asteroid, turns):
    cx, cy = ai.game.size_x / 2, ai.game.size_y / 2
    r = point_dis(asteroid.x, asteroid.y, cx, cy)
    angle = direction(P(cx, cy), P(asteroid.x, asteroid.y))
    delta_angle = -2.0*math.pi/ai.game.turns_to_orbit
    newx = cx + r * math.cos(angle + turns * delta_angle)
    newy = cy + r * math.sin(angle + turns * delta_angle)
    return newx, newy

def direction(obj, target):
    return math.atan2(target.y - obj.y, target.x - obj.x)

def move_toward_asteroid(obj, target):
    d = dis(obj, target)
    turns = int(d / obj.job.moves)
    x = target.next_x(turns)
    y = target.next_y(turns)
    return move_toward(obj, P(x, y))

def move_toward(ai, obj, target, radius=None):
    i = intermediate_point(ai, obj, target)
    target = i or target
    if radius is None:
        radius = obj.job.range + target.radius
    dir = direction(obj, target)
    d = dis(obj, target)
    d = max(0, d - radius)
    d = min(obj.moves-0.1, d)
    if d <= 0:
        return True
    x = obj.x + d * math.cos(dir)
    y = obj.y + d * math.sin(dir)
    #x, y = clamp(ai, P(x, y))
    return obj.move(x, y)

def dash_toward(ai, obj, target, radius=None, maintain_energy=1):
    if radius is None:
        radius = obj.job.range + target.radius
    i = intermediate_point(ai, obj, target)
    if i:
        print('collide', obj.x, obj.y, target.x, target.y)
    target = i or target
    dir = direction(obj, target)
    d = dis(obj, target)
    d = max(0, d - radius)
    useful_energy = max(0, obj.energy - max(maintain_energy, 1))
    d = min(useful_energy * ai.game.dash_distance, d)
    if d <= 0:
        return True
    x = obj.x + d * math.cos(dir)
    y = obj.y + d * math.sin(dir)
    #x, y = clamp(P(x, y))
    return obj.dash(x, y)

def nearest(center, objs):
    nearest_d = 99999999999999999999
    nearest_obj = None
    for obj in objs:
        d = dis(center, obj)
        if d < nearest_d:
            nearest_d = d
            nearest_obj = obj
    return nearest_obj, nearest_d

def clamp(ai, p):
    x = min(ai.game.size_x-1, max(0, p.x))
    y = min(ai.game.size_y-1, max(0, p.y))
    return P(x, y)

def inside(ai, p):
    return 0 < p.x < ai.game.size_x and 0 < p.y < ai.game.size_y

def clamp_line(ai, from_, to):
    d = dis(from_, to)
    dir = direction(from_, to)
    while not inside(ai, to) and d:
        d -= 20
        x = from_.x + d * math.cos(dir)
        y = from_.y + d * math.sin(dir)
        to = P(x, y)
    return to


#def clamp_line(ai, from, to):
#    m = (to.y - from.y) / (to.x - from.x+0.00001)
#    b = to.y - m * to.x
#    if to.y < 0:
#        return P(-b * (to.y - from.y) / (to.x - from.x), 0)
#    elif to.y > ai.game.size_y:
#        return P(ai.game.size_y - b * (to.y - from.y)
#        to.x = 
#        to.y
#    if not inside(ai, to):
#        if 
#        return 
#    return to

def intermediate_point(ai, u, target):
    sun = ai.game.bodies[2]
    clearence = sun.radius+ai.game.ship_radius+1
    if not line_intersect(u.x, u.y, target.x, target.y, sun.x, sun.y, clearence):
        return None
    d = dis(u, target)
    angle = direction(u, target)
    for delta_angle_deg in range(1, 90, 4):
        for sign in [1, -1]:
            delta_angle = delta_angle_deg / 180. * math.pi * sign
            tx = u.x + d*math.cos(angle + delta_angle)
            ty = u.y + d*math.sin(angle + delta_angle)
            if not line_intersect(u.x, u.y, tx, ty, sun.x, sun.y, clearence):
                #return clamp(ai, P(tx, ty))
                clamped = clamp_line(ai, u, P(tx, ty))
                return clamped
    print('This SHOULD NOT HAPPEN')
    return None

def line_intersect(ax, ay, bx, by, cx, cy, r):
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    c = ax**2 + ay**2 - r**2
    b = 2*(ax*(bx - ax) + ay*(by - ay))
    a = (bx - ax)**2 + (by - ay)**2
    disc = b**2 - 4*a*c
    if disc <= 0:
        return False
    sqrtdisc = disc**0.5
    t1 = (-b + sqrtdisc)/(2*a)
    t2 = (-b - sqrtdisc)/(2*a)
    return (0 < t1 < 1) or (0 < t2 < 1)

def away_y(ai, y, distance=None):
    if distance is None:
        distance = ai.game.size_y / 2 - 50
    if y < ai.game.size_y / 2:
        return ai.game.size_y / 2 + distance
    else:
        return ai.game.size_y / 2 - distance

def dis(obj1, obj2):
    return ((obj2.x - obj1.x)**2 + (obj2.y - obj1.y)**2)**0.5

def point_dis(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

    # <<-- /Creer-Merge: functions -->>
