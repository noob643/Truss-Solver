#! python3
#main.py - file that assembles all data, and performs calculation
from definition import Node, Element, Support
from analysis_inputs import nodes_data, elements_data, supports_data

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
for i in range(len(nodes)*2):
    row = []
    for z in range(len(nodes)*2):
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
        
