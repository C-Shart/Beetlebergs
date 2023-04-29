import arcade
import math
import random
from statemachine import StateMachine, State
from stats_manager import StatsManager
from team_color import TeamColor

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
SFXPATH_BEETLE_HIT = "Assets/Sound/SFX/impact2_noisecollector.wav"
SFXPATH_BEETLE_DEAD = "Assets/Sound/SFX/beetle_dead_mixkit.wav"

BEETLE_SCALING = 1
BEETLE_MOVE_FORCE = 175
BEETLE_ROTATION_SPEED = math.pi * 1.5
BEETLE_ROTATION_EPSILON = math.pi / 90.0
DEFAULT_HIT_POINTS = 13
DEFAULT_MAX_FORWARD = 150.0
DEFAULT_MAX_SIDEWAYS = 100.0
DEFAULT_MAX_ROTATION = math.pi / 360.0
DEFAULT_AWARENESS = 1
DEFAULT_VISION = 250
DEFAULT_ACCURACY = 25
SEARCH_RANGE = 160
ENGAGEMENT_RANGE = 150
ENGAGEMENT_EPSILON = 10

class Beetle(arcade.Sprite):
    def __init__(self, team, center_x=0, center_y=0):
        path = BEETLE_SPRITE_PATH_GREEN if team.color == TeamColor.GREEN else BEETLE_SPRITE_PATH_RED
        super().__init__(path, BEETLE_SCALING)
        self.team = team
        self.scale = BEETLE_SCALING
        self.center_x = center_x
        self.center_y = center_y
        self.abilities = []
        self.max_hit_points = DEFAULT_HIT_POINTS
        self.hit_points = DEFAULT_HIT_POINTS
        self.max_forward_speed = DEFAULT_MAX_FORWARD
        self.forward_speed = 0.0
        self.max_sideways_speed = DEFAULT_MAX_SIDEWAYS
        self.sideways_speed = 0.0
        self.max_rotation_speed = DEFAULT_MAX_ROTATION
        self.awareness = DEFAULT_AWARENESS
        self.vision = DEFAULT_VISION
        self.accuracy = DEFAULT_ACCURACY
        self.angle = -90.0 if team.color == TeamColor.GREEN else 90.0
        self.force = 0
        self.logic_state_machine = __class__.logic()
        self.target_facing = None
        self.target_moving = None
        self.is_moving = None
        self.x_velocity = 0
        self.y_velocity = 0
        self.move_target = None
        self.strafe_left = None
        self.angle_target = None
        self.facing_cooldown = 0.0
        self.targeted_beetle = None
        self.firing_target = None
        self.known_enemies = None
        self.active = False
        self.spatial_manager = None
        self.sfx_beetle_dead = arcade.load_sound(SFXPATH_BEETLE_DEAD)

        # Commenting out because we will need hit/damage SFX but dunno where that goes yet
        # self.sfx_beetle_hit = arcade.load_sound(BEETLE_SFXPATH_BEETLE_HIT)

    @property
    def physics_engine(self):
        if len(self.physics_engines) > 0:
            return self.physics_engines[0]
        else:
            return None

    def get_sprite_adjusted_angle_deg(_self, angle):
        angle += 90.0 # TODO: Why is this one plus?
        if angle < -180.0:
            angle += 360.0
        return angle

    def get_sprite_adjusted_angle_rad(_self, angle):
        angle -= math.pi / 2.0
        if angle < -math.pi:
            angle += math.pi * 2.0
        return angle

    def get_facing_angle_to_location(self, target_x, target_y):
        delta_x = target_x - self.center_x
        delta_y = target_y - self.center_y
        return self.get_sprite_adjusted_angle_rad(math.atan2(delta_y, delta_x))

    def get_raw_angle_to_location(self, target_x, target_y):
        delta_x = target_x - self.center_x
        delta_y = target_y - self.center_y
        return math.atan2(delta_y, delta_x)

    def get_components_to_location(self, target_x, target_y):
        angle = self.get_raw_angle_to_location(target_x, target_y)
        return (math.cos(angle), math.sin(angle))

    def decide_facing(self, delta_time):
        if not self.angle_target and self.facing_cooldown <= 0.0:
            self.facing_cooldown = 0.0
            self.angle_target = random.uniform(-math.pi, math.pi)
        elif self.facing_cooldown > 0.0:
            self.facing_cooldown -= delta_time

    def decide_position(self):
        if not self.move_target:
            self.move_target = (random.randrange(0, 1280), random.randrange(0, 720))

    def set_facing(self, target_x, target_y):
        self.angle_target = self.get_facing_angle_to_location(target_x, target_y)

    def move_to(self, target_x, target_y):
        self.move_target = (target_x, target_y)
        # TODO: Do we need this anymore if we're just setting move_target?

    def draw(self):
        super().draw()
        for ability in self.abilities:
            ability.draw()

    def on_update(self, delta_time):
        super().on_update(delta_time)

        if self.active:
            current_state = self.logic_state_machine.current_state
            if current_state == __class__.logic.start_idle:
                self.logic_state_machine.start_battle()
            elif current_state == __class__.logic.find_target:
                nearby_sprites = self.spatial_manager.get_nearby_circle(self.center_x, self.center_y, SEARCH_RANGE)
                nearby_enemies = [sprite for sprite in nearby_sprites if isinstance(sprite, Beetle) and sprite.team.color != self.team.color]
                if nearby_enemies:
                    self.targeted_beetle = min(nearby_enemies, key=lambda b: arcade.get_distance(self.center_x, self.center_y, b.center_x, b.center_y))
                    self.move_target = None # Kill state code will handle movement
                    self.logic_state_machine.target_acquired()
                elif not self.move_target:
                    self.move_target = (random.randrange(100, 1180), random.randrange(100, 620))
                    self.set_facing(self.move_target[0], self.move_target[1])
            elif current_state == __class__.logic.kill_target:
                if self.targeted_beetle.hit_points > 0:
                    target = self.targeted_beetle
                    distance_to_target = arcade.get_distance(self.center_x, self.center_y, target.center_x, target.center_y)
                    delta_to_engagement = ENGAGEMENT_RANGE - distance_to_target
                    component_x, component_y = self.get_components_to_location(target.center_x, target.center_y)
                    x_to_move_target = 0.0
                    y_to_move_target = 0.0
                    if abs(delta_to_engagement) > ENGAGEMENT_EPSILON:
                        # pick a move target with some random jitter to encourage slightly different targets between
                        # beetles
                        x_to_move_target = -delta_to_engagement * component_x + random.gauss(sigma=ENGAGEMENT_EPSILON*3)
                        y_to_move_target = -delta_to_engagement * component_y + random.gauss(sigma=ENGAGEMENT_EPSILON*3)
                    else:
                        # Strafe sideways by rotating the vector to the target by 90 degrees (x, y) -> (y, -x)
                        if self.strafe_left is None:
                            self.strafe_left = random.random() < 0.50
                        elif random.random() < 0.065:
                            self.strafe_left = not self.strafe_left
                        x_to_move_target = 3 * ENGAGEMENT_EPSILON * component_y
                        y_to_move_target = -3 * ENGAGEMENT_EPSILON * component_x
                        if not self.strafe_left:
                            x_to_move_target *= -1
                            y_to_move_target *= -1
                    self.move_target = (self.center_x + x_to_move_target, self.center_y + y_to_move_target)
                    self.set_facing(self.targeted_beetle.center_x, self.targeted_beetle.center_y)
                else:
                    self.strafe_left = None
                    self.targeted_beetle = None
                    self.logic_state_machine.target_eliminated()
            elif current_state == __class__.logic.dead:
                return

        for ability in self.abilities:
            ability.on_update(delta_time)
            ability.active = self.active

        if self.hit_points <= 0:
            arcade.play_sound(self.sfx_beetle_dead)
            self.remove_from_sprite_lists()
            self.spatial_manager.remove(self)
            StatsManager.instance.record_stat(StatsManager.BEETLE_DEAD, team_color=self.team.color)
            if self.logic_state_machine.current_state != __class__.logic.dead:
                self.logic_state_machine.beetle_dead()
        else:
            if self.move_target:
                target_x, target_y = self.move_target
                delta_x = target_x - self.center_x
                delta_y = target_y - self.center_y
                if abs(delta_x) < 10.0 and abs(delta_y) < 10.0:
                    self.move_target = None
                    self.physics_engine.set_velocity(self, (0.0 , 0.0))
                else:
                    x_component, y_component = self.get_components_to_location(target_x, target_y)
                    x_velocity = x_component * BEETLE_MOVE_FORCE
                    y_velocity = y_component * BEETLE_MOVE_FORCE
                    self.physics_engine.set_velocity(self, (x_velocity, y_velocity))
            else:
                self.physics_engine.set_velocity(self, (0.0 , 0.0))

            body = self.physics_engine.sprites[self].body
            if self.angle_target:
                while body.angle > math.pi:
                    body.angle -= 2.0 * math.pi
                while body.angle < -math.pi:
                    body.angle += 2.0 * math.pi

                delta_rotation = self.angle_target - body.angle

                # If the rotation delta is more than 180 degrees, then choose the equivalent acute rotation
                if delta_rotation > math.pi:
                    delta_rotation = -(2.0 * math.pi - delta_rotation)
                elif delta_rotation < -math.pi:
                    delta_rotation = 2.0 * math.pi + delta_rotation

                if abs(delta_rotation) < BEETLE_ROTATION_EPSILON:
                    self.angle_target = None
                    body.angular_velocity = 0.0
                    self.facing_cooldown = 0.5
                elif delta_rotation >= 0.0:
                    body.angular_velocity = BEETLE_ROTATION_SPEED
                else:
                    body.angular_velocity = -BEETLE_ROTATION_SPEED
            else:
                body.angular_velocity = 0.0

    def damage(self, damage):
        self.hit_points -= damage

    class logic(StateMachine):
        start_idle = State(initial=True)
        find_target = State()
        kill_target = State()
        dead = State(final=True)

        start_battle = start_idle.to(find_target)
        target_acquired = find_target.to(kill_target)
        target_eliminated = kill_target.to(find_target)
        beetle_dead = start_idle.to(dead) | find_target.to(dead) | kill_target.to(dead)

        def on_start_battle(self):
            # print("Starting Battle! Looking for Target...")
            pass

        def on_target_acquired(self):
            # print("Acquired target! Eliminating Target...")
            pass

        def on_target_eliminated(self):
            # print("Target Eliminated! Looking for Target...")
            pass

        def on_beetle_dead(self):
            print("RIP.")