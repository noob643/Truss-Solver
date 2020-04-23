# Write your code here :-)
import math
import numpy as np
import copy

class Support:
    supportCount=0

    def __init__(self, point, sup_type):
        self.point=point
        self.sup_type=sup_type

    def sup_cols_rows(self):
        if self.sup_type=='PIN':
            return[self.point*2-1, self.point*2]
        if self.sup_type=='ROLLERX':
            return[self.point*2-1]
        else:
            return[self.point*2]


class Point:
    pointCount=0

    def __init__(self, name, x, y, serial, xforce, yforce):
        self.name=name
        self.x=x
        self.y=y
        self.serial=serial
        self.xforce=xforce
        self.yforce=yforce
        Point.pointCount+=1

    def __del__(self):
        Point.pointCount-=1
        class_name = self.name
        #print (class_name, "deleted")

    def coordinates(self):
        print('Coordinate for X: ',self.x,'\nCoordinate for Y: ',self.y)

    def xy(self):
        return [self.x, self.y]

    def force(self):
        return [self.xforce, self.yforce]

    def force_display(self):
        print('Applied forces at point '+str(self.name+1)+"""
        Fx = """ +str(self.xforce)+"""kN
        Fy = """ +str(self.yforce)+'kN')



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
        sin_alpha = (self.starty-self.endy)/self.length()
        cos_alpha = (self.startx-self.endx)/self.length()
        return [sin_alpha, cos_alpha]

    def stiffness(self):
        k=self.area*self.youngs/self.length()
        return k

    def connectivity(self):
        return [self.startpos, self.endpos]

dictionary = {
            'p1': [0, 0, 0, 0],
            'p2': [3, 0, 10, -10],
            'p3': [6, 0, 0, 0],
            'p4': [1.5, 3, 0, 0],
            'p5': [4.5, 3, 0, 0]
            }

all_points = []
for i in range(len(list(dictionary.items()))):
    all_points.append(
            Point(i,
            list(dictionary.items())[i][1][0],
            list(dictionary.items())[i][1][1],
            list(enumerate(list(dictionary.values())))[i][0],
            list(dictionary.items())[i][1][2],
            list(dictionary.items())[i][1][3]
            ))



dictionary_element = {
                    'elem1': [1, 4, 1],
                    'elem2': [4, 5, 1],
                    'elem3': [5, 3, 1],
                    'elem4': [2, 4, 1],
                    'elem5': [2, 5, 1],
                    'elem6': [1, 2, 1],
                    'elem7': [2, 3, 1]
                    }
all_elements = []
for i in range(len(list(dictionary_element.items()))):
    all_elements.append(
            steelElement(i+1,
            all_points[list(dictionary_element.items())[i][1][0]-1],
            all_points[list(dictionary_element.items())[i][1][1]-1],
            list(dictionary_element.items())[i][1][2]
            ))

supports ={
        'support1': [1, 'PIN'],
        'support2': [3, 'PIN']
        }
all_supports=[]
for i in range(len(list(supports.items()))):
    all_supports.append(
            Support(
            list(supports.values())[i][0],
            list(supports.values())[i][1]
            ))



blank_smatrix=[]
for y in range(len(all_points)*2):
    row=[]
    for x in range(len(all_points)*2):
        row.append(0.0)
    blank_smatrix.append(row)

# create overall stiffenss matrix for the truss
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
# create force vector matrix
# create empty force matrix

all_forces=[]
for i in all_points:
    all_forces+=i.force()
force_matrix=[]
for z in range(len(all_forces)):
    force_matrix.append([all_forces[z]])
#print(force_matrix)

for z in range(8):
    print(str(z+1).rjust(5),end='|')
print()
print('------------------------------------------------')
for i in blank_smatrix:
    for z in i:
        print(str(round(z,2)).rjust(5),end='|')
    print()

sup_to_del=[]
for elem in all_supports:
    sup_to_del+=elem.sup_cols_rows()
sup_to_del.sort(reverse=True)


analysis_matrix=copy.deepcopy(blank_smatrix)

for z in range(len(analysis_matrix)):
    for i in sup_to_del:
        del analysis_matrix[z][i-1]
        

for i in sup_to_del:
    del analysis_matrix[i-1]
    del force_matrix[i-1]
#calculate displacements
A=np.array(analysis_matrix)
x=np.array(force_matrix)
B=np.linalg.solve(A, x)
val_to_ins=sorted(sup_to_del)
B = B.tolist()
B_full=B
displacement=B_full
for i in val_to_ins:
    B_full.insert(i-1, [0.0])
B_full=np.array(B_full)
#print(B_full)

#calculate reactions
reactions_matrix=np.dot(blank_smatrix, B_full)
#reactions_matrix=reactions_matrix.tolist()
#print(reactions_matrix)

#element force calculation
all_elements_force=[]
for i in all_elements:
    force=np.dot(i.stiffness()*np.array(
    [i.orientation()[1],i.orientation()[0],-i.orientation()[1],-i.orientation()[0]]
    ),(
    1/(i.area*i.youngs)
    )*np.array(
    [displacement[i.startpos*2],displacement[i.startpos*2+1],displacement[i.endpos*2],displacement[i.endpos*2+1]]))
    all_elements_force.append(force)
print(all_elements_force)
