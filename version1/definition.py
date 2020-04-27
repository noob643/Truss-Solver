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
        self.disp=''#will be modified after calculating results
        Node.nodeCount+=1

    def p(self):
        return('Node '+str(self.name)+' X: '+str(self.x)+' Y: '+str(self.y)+'\n')

    def xy(self):
        return [self.x, self.y]
    
    def r(self):
        n=[]
        for i in self.disp:
            n.append('Loadcase     :'+str(i)+'\nX-disp       :'+str(round(self.disp[i][0]*1000,2))+'mm'+'\nY-disp       :'+str(round(self.disp[i][1]*1000,2))+'mm\n\n')
        return n    
        
        

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
        if strength == '': #Input in (N/mm2)
            self.strength=float(material_dict[self.material][0])*10**6
        else:
            self.strength=float(strength)*10**6
        if youngs == '': #Input in (N/mm2)
            self.youngs=float(material_dict[self.material][1])*10**6
        else:
            self.youngs=float(youngs)*10**6
        if density == '': #Input in (kN/m3)
            self.density=float(material_dict[self.material][2])*10**3
        else:
            self.density=float(density)*10**3
        if section == '' or section[0]=='USER': #Input in m2
            self.section = 'USER'
            if section =='':
                self.area = 0.01
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
        self.sw = [self.startpos, 0, self.weight/2, self.endpos, 0, self.weight/2]
        self.force = ''#will be updated after analysis
        Element.elemCount+=1

    #properties
    def p(self):
        return(
        '\n\nElement name     :'+str(self.name)+
        '\nStart Node       :'+str(self.startpos)+' with coordinates '+str(self.point_start.xy())+
        '\nEnd Node         :'+str(self.endpos)+' with coordinates '+str(self.point_end.xy())+
        '\nMaterial         :'+str(self.material)+
        '\nStrength         :'+str(self.strength/10**6)+'N/mm2'+
        '\nYoungs Modulus   :'+str(self.youngs/10**6)+'N/mm2'+
        '\nDensity          :'+str(self.density/1000)+'kN/m3'+
        '\nSection          :'+str(self.section)+
        '\nArea             :'+str(self.area*10000)+'cm2'+
        '\nLength           :'+str(round(self.length,2))+'m'+
        '\nMass             :'+str(round(self.weight/9.81,2))+'kg')
        

    #results
    def r(self):
        n=[]
        for i in self.force:
            n.append('\n\nLoadcase     :'+str(i)+
            '\nAxial Force  :'+str(round(self.force[i]/1000,2))+'kN')
        return n

#Definition of supports
class Support:
    supportCount=0

    def __init__(self, point, sup_type):
        self.point=point
        self.sup_type=sup_type
        self.res='' # will be modified after analysis is complete
        Support.supportCount+=1

    def sup_cols_rows(self):
        if self.sup_type=='PIN':
            return[(self.point.name-1)*2, (self.point.name-1)*2+1]
        if self.sup_type=='ROLLERX':
            return[(self.point.name-1)*2]
        else:
            return[(self.point.name-1)*2+1]
    
    def p(self):
        return('\nNode '+str(self.point.name)+' Support Type: '+str(self.sup_type))
    
    def r(self):
        n=[]
        for i in self.res:
            n.append('\nLoadcase     :'+str(i)+'\nX-reaction   :'+str(round(self.res[i][0]/1000,2))+' kN\nY-reaction   :'+str(round(self.res[i][1]/1000,2))+' kN\n')
        return n

#Definition of loads
class Load:
    loadCount=0

    def __init__(self, point, loadx, loady):
        self.point=point
        self.x=loadx
        self.y=loady
        Load.loadCount+=1
