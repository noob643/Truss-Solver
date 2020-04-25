#! python3
# definition.py creates definitions for Node, Elements and Supports
from external_data import sections_dict, material_dict
import math

# Definition for nodes
class Node:
    nodeCount=0

    def __init__(self, name, x, y):
        self.name=int(name)
        self.x=float(x)
        self.y=float(y)
        Node.nodeCount+=1
        
    def coordinates(self):
        print('Node',self.name,'\nX:',self.x,'\nY:',self.y)

    def xy(self):
        return [self.x, self.y]

#Definition of elements
class Element:
    
    elemCount =0

    def __init__(self, name, point_start, point_end, material='STEEL', strength='',
                youngs='', density='', section=''):
        self.name=name
        self.point_start=point_start
        self.point_end=point_end
        self.startx=point_start.xy()[0]
        self.starty=point_start.xy()[1]
        self.endx=point_end.xy()[0]
        self.endy=point_end.xy()[1]
        self.startpos=point_start.name
        self.endpos=point_end.name
        self.material=material
        if strength == '':
            self.strength=float(material_dict[self.material][0])
        else:
            self.strength=float(strength)
        if youngs == '':
            self.youngs=float(material_dict[self.material][1])
        else:
            self.youngs=float(youngs)
        if density == '':
            self.density=float(material_dict[self.material][2])
        else:
            self.density=float(density)
        if section == '' or section[0]=='USER':
            self.section = 'USER'
            if section =='':
                self.area = 0.1
            else:
                self.area = float(section[1])
        else:
            self.section = section[0],section[1]
            self.area = float(sections_dict[section[0]][section[1]])/10000
        self.length = math.sqrt((self.endx-self.startx)**2+(self.endy-self.starty)**2)
        self.weight = self.area*self.length*self.density
        self.sin = (self.starty-self.endy)/self.length
        self.cos = (self.startx-self.endx)/self.length
        self.k = self.area*self.youngs/self.length
        Element.elemCount+=1
        
    #properties
    def p(self):
        print('Element name     :',self.name)
        print('Start Node       :',self.startpos,'with coordinates',self.point_start.xy())
        print('End Node         :',self.endpos,'with coordinates',self.point_end.xy())
        print('Material         :',self.material)
        print('Strength         :',self.strength,'N/mm2')
        print('Youngs Modulus   :',self.youngs,'N/mm2')
        print('Density          :',self.density,'kN/m3')
        print('Section          :',self.section)
        print('Area             :',self.area*10000,'cm2')
        print('Length           :',round(self.length,2),'m')
        print('Mass             :',round(self.weight/9.81*1000,2),'kg')
        print()

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


