#! python3
#main.py - file that assembles all data, and performs calculation
from definition import Node, Element, Support, Load
from analysis_inputs import nodes_data, elements_data, supports_data, loadcases
import numpy as np
import copy
# Create truss nodes
nodes=[]
for i in nodes_data:
    nodes.append(Node(i, nodes_data[i][0], nodes_data[i][1]))
nodes_dict={}
for i in nodes:
    nodes_dict.setdefault(i.name, i)

# Create truss elements
elements=[]
for i in elements_data:
    elements.append(Element(i,nodes_dict[elements_data[i][0]],
        nodes_dict[elements_data[i][1]],
        elements_data[i][2], elements_data[i][3],
        elements_data[i][4],elements_data[i][5],
        elements_data[i][6]))
            
# Create supports
supports=[]
for i in supports_data:
    supports.append(Support(nodes_dict[int(i)], supports_data[i]))

# Create blank stiffness matrix
st_mat = []
for i in range(max(list(nodes_dict.keys()))*2):
    row = []
    for z in range(max(list(nodes_dict.keys()))*2):
        row.append(0.0)
    st_mat.append(row)

#Populate stiffness matrix
for i in elements:
    for z in [i.startpos, i.endpos]:
        st_mat[(z-1)*2][(z-1)*2]+=i.k*i.cos**2
        st_mat[(z-1)*2][(z-1)*2+1]+=i.k*i.cos*i.sin
        st_mat[(z-1)*2+1][(z-1)*2]+=i.k*i.cos*i.sin
        st_mat[(z-1)*2+1][(z-1)*2+1]+=i.k*i.sin**2

    st_mat[(i.startpos-1)*2][(i.endpos-1)*2]+=-i.k*i.cos**2
    st_mat[(i.startpos-1)*2][(i.endpos-1)*2+1]+=-i.k*i.cos*i.sin
    st_mat[(i.startpos-1)*2+1][(i.endpos-1)*2]+=-i.k*i.cos*i.sin
    st_mat[(i.startpos-1)*2+1][(i.endpos-1)*2+1]+=-i.k*i.sin**2

    st_mat[(i.endpos-1)*2][(i.startpos-1)*2]+=-i.k*i.cos**2
    st_mat[(i.endpos-1)*2][(i.startpos-1)*2+1]+=-i.k*i.cos*i.sin
    st_mat[(i.endpos-1)*2+1][(i.startpos-1)*2]+=-i.k*i.cos*i.sin
    st_mat[(i.endpos-1)*2+1][(i.startpos-1)*2+1]+=-i.k*i.sin**2

st_mat_full=copy.deepcopy(st_mat)
#Create load vectors (including self weigth based on member areas
#Create empty self weight matrix
self_weight=[]
for i in range(max(list(nodes_dict.keys()))*2):
    self_weight.append([0.0])
    
#Populate self weight matrix with element weights    
for i in elements:
    self_weight[(i.sw[0]-1)*2][0]+=-i.sw[1]
    self_weight[(i.sw[0]-1)*2+1][0]+=-i.sw[2]
    self_weight[(i.sw[3]-1)*2][0]+=-i.sw[4]
    self_weight[(i.sw[3]-1)*2+1][0]+=-i.sw[5]
    
#Create loading vectors for each loadcase
loadings = {}
for i in list(loadcases.keys()):
    
    loading=[]
    
    for z in range(max(list(nodes_dict.keys()))*2):
        loading.append([0.0])
    
    for z in loadcases[i]:
        loading[(int(z)-1)*2][0]+=float(loadcases[i][z][0])*1000 #multiply to convert from kN to N
        loading[(int(z)-1)*2+1][0]+=float(loadcases[i][z][1])*1000

    for z in range(len(loading)):
        loading[z][0]+=self_weight[z][0]
    loadings.setdefault(i, loading)

#Define supported nodes
support_nodes=[]
for i in supports:
    support_nodes+=i.sup_cols_rows()
loadings_full=copy.deepcopy(loadings['1'])

#Modify loading vectors and stiffness matrix based on support conditions
for i in list(reversed(support_nodes)):
    for z in range(len(st_mat)):
        del st_mat[z][i]
    del st_mat[i]
    del loadings['1'][i]
    
#Convert lists to matrices and find displacements
A=np.array(st_mat)
B=np.array(loadings['1'])
disp=np.linalg.solve(A, B) #displacements

#Insert missing support nodes
disp = disp.tolist()
for i in list(sorted(support_nodes)):
    disp.insert((i),[0.0])

#Record displacement against node instances    
for i in nodes:
    setattr(i,'dispx',disp[(i.name-1)*2][0])
    setattr(i,'dispy',disp[(i.name-1)*2+1][0])

#Calculate support reactions
disp=np.array(disp)
R=np.dot(st_mat_full, disp)
R.tolist()
for i in supports:
    setattr(i,'rx',R[(i.point.name-1)*2][0])
    setattr(i,'ry',R[(i.point.name-1)*2+1][0])

#Calculate force in elements
for i in elements:
    lm=[i.k*i.cos, i.k*i.sin, i.k*(-i.cos), i.k*(-i.sin)]
    disp1=[disp.tolist()[(i.startpos-1)*2],disp.tolist()[(i.startpos-1)*2+1],disp.tolist()[(i.endpos-1)*2],disp.tolist()[(i.endpos-1)*2+1]]
    F=np.dot(np.array(lm),np.array(disp1))
    setattr(i,'force',F[0])
  
