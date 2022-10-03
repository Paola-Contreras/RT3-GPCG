from math import  pi, acos, atan2
import math_lib as ml 
import numpy as np

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texcoords = texcoords
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0, texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = ml.subtract(self.center, orig)
        tca = ml.dot(L, dir)

        #Magnitud de un vector 
        Sum= (L[0] **2 + L[1]**2 + L[2]**2)**0.5
        d = (Sum ** 2 - tca ** 2) ** 0.5


        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        mul = []
        for j in range(len(dir)):
            res = t0 * dir[j]
            mul.append(res)

        P = ml.add(orig, t0 * mul)
        normal = ml.subtract(P, self.center)
        normal = ml.normalized(normal)

        u = 1 - ((atan2(normal[2], normal[0]) / (2 * pi)) + 0.5)
        v = acos(-normal[1]) / pi

        uvs = (u,v)

        return Intersect(distance = t0,
                         point = P,
                         normal = normal,
                         texcoords = uvs,
                         sceneObj = self)

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = normal / np.linalg.norm(normal)
        #self.normal = ml.normalized(normal)
        self.material = material


    def ray_intersect(self, orig, dir):
        denom = ml.dot(dir, self.normal)

        #Distancia = ((planePos - oriRayo) o planeNormal) / (direccionRayo o normal) => para calcular la distnacia a la que va a encontrar
        
        if abs(denom) > 0.0001: 
            num = ml.dot(ml.subtract(self.position, orig), self.normal)

            t = num / denom
            
            if t > 0:
                # P = O + t0 * D
                P2 = []
                for k in range(len(dir)):
                    res = t * dir[k]
                    P2.append(res)

                P = ml.add(orig,P2)
                return Intersect(distance = t,
                                point = P,
                                normal = self.normal,
                                texcoords = None,
                                sceneObj = self)
        return None

class AABB(object):

    # Axis Aligned Bounding Box
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material

        self.planes = []
        
        halfSizes = [0,0,0]

        halfSizes[0] = size[0] / 2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2

        # Sides
        self.planes.append(Plane(ml.add(position, (halfSizes[0],0,0)), (1,0,0), material))
        self.planes.append(Plane(ml.add(position, (-halfSizes[0],0,0)), (-1,0,0), material))

        # Up and Down
        self.planes.append(Plane(ml.add(position, (0,halfSizes[1],0)), (0,1,0), material))
        self.planes.append(Plane(ml.add(position, (0,-halfSizes[1],0)), (0,-1,0), material))

        # Front and Back
        self.planes.append(Plane(ml.add(position, (0,0,halfSizes[2])), (0,0,1), material))
        self.planes.append(Plane(ml.add(position, (0,0,-halfSizes[2])), (0,0,-1), material))

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])

    #OBB - Oriented Bounding Box


    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                planePoint = planeInter.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:

                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

        if intersect is None:
            return None

        return Intersect(distance = t,
                                point = intersect.point,
                                normal = intersect.normal,
                                texcoords = None,
                                sceneObj = self)

class Disk(object):
    def __init__(self, position, radius, normal, material) :
        self.plane = Plane(position, normal, material)
        self.material = material    
        self.radius = radius

    def ray_intersect(self, orig, dir):
        intersect = self.plane.ray_intersect(orig, dir)
        
        if intersect is None:
            return None
        
        contact = ml.subtract(intersect.point, self.plane.position)
        contact = ml.normalized(contact)


        if contact > self.radius:
            return None
        
        return Intersect(distance = intersect.distance,
                                point = intersect.point,
                                normal = self.normal,
                                texcoords = None,
                                sceneObj = self)