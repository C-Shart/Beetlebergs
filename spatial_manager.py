import arcade

# CONSTANTS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NODE_CAPACITY = 7
MAX_LEVELS = 7

class SpatialManager:
    def __init__(self):
        self.sprites = []
        self.root = None
        self.initialize_nodes()

    def initialize_nodes(self):
        self.root = __class__.node(1, 0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

    def add_sprite(self, sprite):
        self.sprites.append(sprite)
        self.root.insert(sprite)
        sprite.spatial_manager = self

    def add_sprite_list(self, sprite_list):
        for sprite in sprite_list:
            self.add_sprite(sprite)

    def remove(self, sprite):
        self.sprites.remove(sprite)
        sprite.spatial_manager = None

    def on_update(self, delta_time):
        self.initialize_nodes()
        for sprite in self.sprites:
            self.root.insert(sprite)

    def get_nearby(self, x, y, range=250.0):
        side = range / 2.0
        x_min = x - side
        x_max = x + side
        y_min = y - side
        y_max = y + side
        return self.root.retrieve_rectangle(x_min, x_max, y_min, y_max)

    def get_nearby_circle(self, x, y, radius=125.0):
        rectangle_results = self.root.retrieve_rectangle(x - radius, x + radius, y - radius, y + radius)
        results = []
        for result in rectangle_results:
            if arcade.get_distance(x, y, result.center_x, result.center_y) <= radius:
                results.append(result)
        return results if results else None

    class node():
        def __init__(self, level, x_min, x_max, y_min, y_max):
            self.level = 0
            self.x_min = x_min
            self.x_max = x_max
            self.x_split = (x_max - x_min) / 2.0
            self.y_min = y_min
            self.y_max = y_max
            self.y_split = (y_max - y_min) / 2.0
            self.parent = None
            self.northwest = None
            self.northeast = None
            self.southeast = None
            self.southwest = None
            self.sprites = []

        def split(self):
            new_level = self.level + 1
            self.northwest = type(self)(new_level, self.x_min, self.x_split, self.y_split, self.y_max)
            self.northeast = type(self)(new_level, self.x_split, self.x_max, self.y_split, self.y_max)
            self.southeast = type(self)(new_level, self.x_split, self.x_max, self.y_min, self.y_split)
            self.southwest = type(self)(new_level, self.x_min, self.x_split, self.y_min, self.y_split)
            self.northwest.parent = self
            self.northeast.parent = self
            self.southwest.parent = self
            self.southeast.parent = self

            for sprite in self.sprites:
                self.get_quad(sprite.center_x, sprite.center_y).sprites.append(sprite)

            self.sprites.clear()

        def get_quad(self, x, y):
            if y < self.y_split:
                if x < self.x_split:
                    return self.southwest
                else:
                    return self.southeast
            else:
                if x < self.x_split:
                    return self.northwest
                else:
                    return self.northeast

        def insert(self, sprite):
            desired_quad = self.get_quad(sprite.center_x, sprite.center_y)
            if desired_quad:
                desired_quad.insert(sprite)
            else:
                if len(self.sprites) < NODE_CAPACITY or self.level + 1 < MAX_LEVELS:
                    self.sprites.append(sprite)
                elif self.level + 1 < MAX_LEVELS:
                    self.split()
                    desired_quad = self.get_quad(sprite.center_x, sprite.center_y)
                    desired_quad.insert(sprite)

        def retrieve(self, x, y):
            desired_quad = self.get_quad(x, y)
            if desired_quad:
                return desired_quad.retrieve(x, y)
            else:
                return self.sprites

        def retrieve_rectangle(self, x_min, x_max, y_min, y_max):
            if not self.intersects_rectangle(x_min, x_max, y_min, y_max):
                return None
            elif not self.northwest:
                result = []
                for sprite in self.sprites:
                    half_height = sprite.height / 2
                    half_width = sprite.width / 2
                    sprite_x_min = sprite.center_x - half_width
                    sprite_x_max = sprite.center_x + half_width
                    sprite_y_min = sprite.center_y - half_height
                    sprite_y_max = sprite.center_y + half_height
                    if x_max < sprite_x_min or x_min > sprite_x_max or y_max < sprite_y_min or y_min > sprite_y_max:
                        continue
                    else:
                        result.append(sprite)
                return result if result else None
            else:
                nw_sprites = self.northwest.retrieve_rectangle(x_min, x_max, y_min, y_max)
                ne_sprites = self.northeast.retrieve_rectangle(x_min, x_max, y_min, y_max)
                sw_sprites = self.southwest.retrieve_rectangle(x_min, x_max, y_min, y_max)
                se_sprites = self.southeast.retrieve_rectangle(x_min, x_max, y_min, y_max)
                result = []
                if nw_sprites:
                    result.extend(nw_sprites)
                if ne_sprites:
                    result.extend(ne_sprites)
                if sw_sprites:
                    result.extend(sw_sprites)
                if se_sprites:
                    result.extend(se_sprites)
                return result if result else None

        def intersects_rectangle(self, x_min, x_max, y_min, y_max):
            if x_max < self.x_min or x_min > self.x_max or y_max < self.y_min or y_min > self.y_max:
                return False
            else:
                return True
