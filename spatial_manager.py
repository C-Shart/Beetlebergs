from pymunk.vec2d import Vec2d
from arcade import gl

class SpatialManager:
    def __init__(self, capacity, boundary):
        self.capacity = capacity
        self.boundary = boundary
        self.colliders = []

        self.north_west = None
        self.north_east = None
        self.south_west = None
        self.south_east = None

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

        self.north_west = Quadtree(self.capacity, boundary_nw)
        self.north_east = Quadtree(self.capacity, boundary_ne)
        self.south_west = Quadtree(self.capacity, boundary_sw)
        self.south_east = Quadtree(self.capacity, boundary_se)

        for i in range(len(self.colliders)):
            self.north_west.insert(self.colliders[i])
            self.north_east.insert(self.colliders[i])
            self.south_west.insert(self.colliders[i])
            self.south_east.insert(self.colliders[i])

    def insert(self, collider):
        if self.boundary.contains_collider(collider) == False:
            return False

        if len(self.colliders) < self.capacity and self.north_west == None:
            self.colliders.append(collider)
            return True
        else:
            if self.north_west == None:
                self.subdivide()

            if self.north_west.insert(collider):
                return True
            if self.north_east.insert(collider):
                return True
            if self.south_west.insert(collider):
                return True
            if self.south_east.insert(collider):
                return True
            return False

    def query_range(self, _range):
        colliders_in_range = []

        if type(_range) == __class__.Circle:
            if _range.intersects(self.boundary)==True:
                return colliders_in_range
        elif type(_range) == __class__.Rectangle:
            if _range.intersects(self.boundary)==True:
                return colliders_in_range

        if self.boundary.intersects(_range):
            return particlesInRange
        else:
            for collider in self.colliders:
                if _range.contains_collider(collider):
                    colliders_in_range.append(collider)
            if self.north_west != None:
                colliders_in_range += self.north_west.query_range(_range)
                colliders_in_range += self.north_east.query_range(_range)
                colliders_in_range += self.south_west.query_range(_range)
                colliders_in_range += self.south_east.query_range(_range)

# Commenting out Show until we can figure out how to implement
    """ def Show(self, screen):
        self.boundary.Draw(screen)
        if self.north_west != None:
            self.north_west.Show(screen)
            self.north_east.Show(screen)
            self.south_west.Show(screen)
            self.south_east.Show(screen) """

    def on_update(self, delta_time):
        # TODO: Recalculates buckets, adds sprites and spritelists to track
        pass

    def get_nearby(self):
        # TODO: Called after on_update has ran to get objects nearby a certain x, y
        pass

    # Drawing useful ranges
    class Rectangle:
        def __init__(self, position, scale):
            self.position = position
            self.scale = scale
            self.line_thickness = 0

        def contains_collider(self, collider):
            x, y = collider.position
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

        def contains_collider(self, collider):
            x1, y1 = self.position
            x2, y2 = collider.position
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