import math

class Point:
    pointCount=0

    def __init__(self, name, x, y, serial):
        self.name=name
        self.x=x
        self.y=y
        self.serial=serial
        Point.pointCount+=1

    def __del__(self):
        Point.pointCount-=1
        class_name = self.name
        print (class_name, "deleted")

    def coordinates(self):
        print('Coordinate for X: ',self.x,'\nCoordinate for Y: ',self.y)

    def xy(self):
        return [self.x, self.y]


class steelElement:

    elemCount =0

    def __init__(self, name, point_start, point_end, area):
        self.name=name
        self.startx=point_start.xy()[0]
        self.starty=point_start.xy()[1]
        self.endx=point_end.xy()[0]
        self.endy=point_end.xy()[1]
        self.startpos=point_start.serial
        self.endpos=point_end.serial
        self.area=area
        self.density=7800
        self.poi_rat=0.3
        self.youngs=1

        steelElement.elemCount+=1

    def length(self):
        length=math.sqrt((self.endx-self.startx)**2+(self.endy-self.starty)**2)
        return length

    def weight(self):
        weight = self.area*self.length()*self.density
        return weight

    def position(self):
        print('Start at x=',self.startx,' y=',self.starty,'\nEnd at x=',
        self.endx,' y=',self.endy)
    
    def orientation(self):
        sin_alpha = (self.endy-self.starty)/self.length()
        cos_alpha = (self.endx-self.startx)/self.length()
        return [sin_alpha, cos_alpha]
    
    def stiffness(self):
        k=self.area*self.youngs/self.length()
        return k

dictionary = {'p1':[0, 0], 'p2': [0, 3], 'p3': [2.5, 3], 'p4': [2.5, 0]}
all_points = []
for i in range(len(list(dictionary.items()))):
    all_points.append(
            Point(i,
            list(dictionary.items())[i][1][0],
            list(dictionary.items())[i][1][1],
            list(enumerate(list(dictionary.values())))[i][0]
            ))



dictionary_element = {
                    'elem1': [1, 2, 1],
                    'elem2': [1, 4, 1],
                    'elem3': [3, 4, 1],
                    'elem4': [2, 3, 1],
                    'elem5': [2, 4, 1],
                    'elem6': [1, 3, 1],
                    }
all_elements = []
for i in range(len(list(dictionary_element.items()))):
    all_elements.append(
            steelElement(i+1,
            all_points[list(dictionary_element.items())[i][1][0]-1],
            all_points[list(dictionary_element.items())[i][1][1]-1],
            list(dictionary_element.items())[i][1][2]
            ))



blank_smatrix=[]
for y in range(len(all_points)*2):
    row=[]
    for x in range(len(all_points)*2):
        row.append(0)
    blank_smatrix.append(row)


for i in range(len(all_elements)):
    blank_smatrix[all_elements[i].startpos*2][all_elements[i].startpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]**2
    blank_smatrix[all_elements[i].startpos*2][all_elements[i].startpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]
    blank_smatrix[all_elements[i].startpos*2+1][all_elements[i].startpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]
    blank_smatrix[all_elements[i].startpos*2+1][all_elements[i].startpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[0]**2

    blank_smatrix[all_elements[i].endpos*2][all_elements[i].endpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]**2
    blank_smatrix[all_elements[i].endpos*2][all_elements[i].endpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]
    blank_smatrix[all_elements[i].endpos*2+1][all_elements[i].endpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]
    blank_smatrix[all_elements[i].endpos*2+1][all_elements[i].endpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[0]**2

    blank_smatrix[all_elements[i].startpos*2][all_elements[i].endpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]**2*(-1)
    blank_smatrix[all_elements[i].startpos*2][all_elements[i].endpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]*(-1)
    blank_smatrix[all_elements[i].startpos*2+1][all_elements[i].endpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]*(-1)
    blank_smatrix[all_elements[i].startpos*2+1][all_elements[i].endpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[0]**2*(-1)

    blank_smatrix[all_elements[i].endpos*2][all_elements[i].startpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]**2*(-1)
    blank_smatrix[all_elements[i].endpos*2][all_elements[i].startpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]*(-1)
    blank_smatrix[all_elements[i].endpos*2+1][all_elements[i].startpos*2]+=all_elements[i].stiffness()*all_elements[i].orientation()[1]*all_elements[i].orientation()[0]*(-1)
    blank_smatrix[all_elements[i].endpos*2+1][all_elements[i].startpos*2+1]+=all_elements[i].stiffness()*all_elements[i].orientation()[0]**2*(-1)

for i in blank_smatrix:
    print(i)
