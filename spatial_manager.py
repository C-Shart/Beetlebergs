from arcade import gl
from pymunk.vec2d import Vec2d
from math import sqrt

# CONSTANTS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
NODE_CAPACITY = 2

class SpatialManager:
    def __init__(self, capacity, boundary):
        self.capacity = capacity
        self.boundary = boundary
        self.sprites = []
        # TODO: insert way of appending sprites to self.sprites[]

        self.northwest = None
        self.northeast = None
        self.southwest = None
        self.southeast = None

        quadtree = SpatialManager(NODE_CAPACITY, boundary)

    def subdivide(self):
        parent = self.boundary
        boundary_nw = __class__.Rectangle(Vec2d(
                parent.position.x,
                parent.position.y
            ),
            parent.scale/2
        )
        boundary_ne = __class__.Rectangle(Vec2d(
                parent.position.x + parent.scale.x/2,
                parent.position.y
            ),
            parent.scale/2
        )
        boundary_sw = __class__.Rectangle(Vec2d(
                parent.position.x,
                parent.position.y + parent.scale.y/2
            ),
            parent.scale/2
        )
        boundary_se = __class__.Rectangle(Vec2d(
                parent.position.x + parent.scale.x/2,
                parent.position.y + parent.scale.y/2
            ),
            parent.scale/2
        )

        self.northwest = SpatialManager(self.capacity, boundary_nw)
        self.northeast = SpatialManager(self.capacity, boundary_ne)
        self.southwest = SpatialManager(self.capacity, boundary_sw)
        self.southeast = SpatialManager(self.capacity, boundary_se)

        for i in range(len(self.sprites)):
            self.northwest.insert(self.sprites[i])
            self.northeast.insert(self.sprites[i])
            self.southwest.insert(self.sprites[i])
            self.southeast.insert(self.sprites[i])

    def insert(self, sprite):
        if self.boundary.contains_sprite(sprite) == False:
            return False

        if len(self.sprites) < self.capacity and self.northwest == None:
            self.sprites.append(sprite)
            return True
        else:
            if self.northwest == None:
                self.subdivide()

            if self.northwest.insert(sprite):
                return True
            if self.northeast.insert(sprite):
                return True
            if self.southwest.insert(sprite):
                return True
            if self.southeast.insert(sprite):
                return True
            return False

    def query_range(self, range):
        sprites_in_range = []

        if type(range) == __class__.Circle:
            if range.intersects(self.boundary)==True:
                return sprites_in_range
        elif type(range) == __class__.Rectangle:
            if range.intersects(self.boundary)==True:
                return sprites_in_range

        if self.boundary.intersects(range):
            return sprites_in_range
        else:
            for sprite in self.sprites:
                if range.contains_sprite(sprite):
                    sprites_in_range.append(sprite)
            if self.northwest != None:
                sprites_in_range += self.northwest.query_range(range)
                sprites_in_range += self.northeast.query_range(range)
                sprites_in_range += self.southwest.query_range(range)
                sprites_in_range += self.southeast.query_range(range)

        # Commenting out Show until we can figure out how to implement
    """ def Show(self, screen):
        self.boundary.Draw(screen)
        if self.north_west != None:
            self.north_west.Show(screen)
            self.north_east.Show(screen)
            self.south_west.Show(screen)
            self.south_east.Show(screen) """


    class QuadtreeNode:
        def __init__(self):
            boundary = SpatialManager.Rectangle(Vec2d(0,0), Vec2d(SCREEN_WIDTH, SCREEN_HEIGHT))

            # TODO: create nodes
            pass


    # Drawing useful ranges
    class Rectangle:
        def __init__(self, position, scale):
            self.position = position
            self.scale = scale
            self.line_thickness = 0

        def contains_sprite(self, sprite):
            x, y = sprite.position
            bx, by = self.position
            w, h = self.scale
            if x >= bx and x <= bx+w and y >= by and y <= by+h:
                return True
            else:
                return False

        def intersects(self, _range):
            x, y = self.position
            w, h = self.scale
            xr, yr = _range.position
            wr, hr= _range.scale
            if xr > x+w or xr+wr < x-w or yr > y+h or yr+hr < y-h:
                return True
            else:
                return False

        # Commenting out Draw methods for now until I can figure out how to get them drawn properly.
        """ def Draw(self):
            x, y = self.position
            w, h = self.scale
            gl.geometry.screen_rectangle(self.position[0], self.scale[0], self.position, self.line_thickness) """

    class Circle:
        def __init__(self, position, radius):
            self.position = position
            self.radius = radius
            self.sqradius = self.radius * self.radius
            self.scale = None
            self.line_thickness = 0

        def contains_sprite(self, sprite):
            x1, y1 = self.position
            x2, y2 = sprite.position
            distance = pow(x2-x1, 2) + pow(y2-y1, 2)
            if distance <= self.sqradius:
                return True
            else:
                return False

        def intersects(self, _range):
            x1, y1 = self.position
            x2, y2 = _range.position
            w, h = _range.scale
            r = self.radius
            distance_x, distance_y = abs(x2-x2), abs(y2-y1)

            edges = pow(distance_x-w, 2) + pow(distance_y-h, 2)

            if distance_x > (r+w) or distance_y > (r+h):
                return False
            
            if distance_x <= w or distance_y <= h:
                return True
            
            return (edges <= self.sqradius)

        # Commenting out Draw methods for now until I can figure out how to get them drawn properly.
        """ def Draw(self):
            gl.geometry.????() """

    def on_update(self, delta_time):
        # TODO: Recalculates buckets, adds sprites and spritelists to track
        pass

    def get_nearby(self):
        # TODO: Called after on_update has ran to get objects nearby a certain x, y
        pass