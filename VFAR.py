print("God is Great")
#Creating and initialising ECRUD Matrix
Site=8
Attribute=10
#C=1 U=2 R=3 D=4
ECRUD_Matrix=[[1,3,2,0,0,0,0,0,0,0,0,0,3,3,4,1,2,3,0,0,0,0,0,0],
              [0,0,0,1,[1,3],4,0,0,0,[3,2],[1,2],4,[1,2,3],3,4,0,0,0,0,0,0,0,0,0],
              [0,0,0,[1,2,3],3,4,0,0,0,0,0,0,[1,3],4,2,0,0,0,[2,4],3,3,3,3,2],
              [0,0,0,0,0,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,1,3,4],
              [2,3,4,0,0,0,0,0,0,0,0,0,1,3,[2,4],3,3,2,0,0,0,0,0,0],
              [0,0,0,0,0,0,1,3,4,0,0,0,0,0,0,0,0,0,0,0,0,1,2,4],
              [2,4,3,0,0,0,0,0,0,1,2,4,1,3,4,0,0,0,0,0,0,0,0,0],
              [0,0,0,1,3,4,0,0,0,4,4,3,1,3,2,0,0,0,0,0,0,0,0,0],
              [0,0,0,1,3,4,0,0,0,0,0,0,1,3,[2,4],0,0,0,[1,2,3],[1,2,3],3,3,3,4],
              [0,0,0,0,0,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,1,3,4]]
#________________________Creating Attribue Site Usage Matrix____________________________
Asum_Matrix = [[0 for i in range(8)] for j in range(10)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if index%3 is not 0:
            index+=1
            continue
        if value is not 0:
            Asum_Matrix[Index_of_List][int(index/3)]=1
            index+=1
        else:
            index+=1
    Index_of_List+=1

#_________________________Creating Attribure Similarity Matrix__________________________
Asm_matrix=[[0 for i in range(10)] for j in range(10)]

def Asm_Matrix_Value_Generator(A,B):
    C=[0 for i in range(8)]
    for i in range(8):
        C[i]=A[i]*B[i]

    return C.count(1)

for i in range(10):
    for j in range(10):
        if i==j:
            Asm_matrix[i][j]=0
        else:
            Asm_matrix[i][j]=Asm_Matrix_Value_Generator(Asum_Matrix[i],Asum_Matrix[j])

#_________________________Now Constructing Spanning tree On Asm_Matrix____________________________

Queue=[0,1,2,3,4,5,6,7,8,9]
Nodes_in_ST=[]
Nodes_in_ST_WithRoot={}
Node_distance_lis={}              #its a dictionary
Nodes_in_ST.append(Queue.pop(0))  #removing root index
while Queue != []:                #until all the attributes are not added in tree
    Node_distance_lis.clear()
    for NodeFromQ in Queue:
        E={NodeFromQ:{'distance':0,'root':0}}
        Node_distance_lis.update(E)

    for Node in Nodes_in_ST:
        for NodeFromQ in Queue:
            if(Asm_matrix[Node][NodeFromQ] > Node_distance_lis[NodeFromQ]['distance'] ):
                Node_distance_lis[NodeFromQ]['distance']=Asm_matrix[Node][NodeFromQ]
                Node_distance_lis[NodeFromQ]['root']=Node
    Max=0
    for key,value in Node_distance_lis.items():
        if Node_distance_lis[key]['distance']>Max:
            Max=Node_distance_lis[key]['distance']
            MaxKey=key

    Nodes_in_ST.append(MaxKey)
    Queue.remove(MaxKey)
    E={MaxKey:Node_distance_lis[MaxKey]['root']}
    Nodes_in_ST_WithRoot.update(E)

print("\t\t\t\t\t\tMinimum Spanning Tree Details\n","\n",repr("From").rjust(5),repr("To").rjust(5),repr("Weight").rjust(5))
for key,value in Nodes_in_ST_WithRoot.items():
    print(repr(key).rjust(5),repr(value).rjust(5),repr(Asm_matrix[key][value]).rjust(5))
#print(Nodes_in_ST_WithRoot)
#___________Remember partitioning is left__________________________________________
#Node_in_ST_WithRoot contains info in the form of {node:root} eg {1:2} so its edge info
#Node_distnace_lis contains info in the form of {key:{distance:d,root:r}}
#which tells node 'key' is at distance d from node 'r'
#_________________________________________________________________________________

#______________________Creating Attribute Manipulate Matrix_______________________
Amm_Matrix= [[0 for i in range(10)] for j in range(8)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if value is not 0:
            if type(value)is list:          #this lis is data type lis
                for i in value:
                    if i is 1 or i is 2 or i is 4:
                        Amm_Matrix[int(index/3)][Index_of_List]+=1
            else:
                if value is 1 or value is 2 or value is 4:
                     Amm_Matrix[int(index/3)][Index_of_List]+=1
            index+=1
        else:
            index+=1
    Index_of_List+=1

#print(Amm_Matrix)
#______________________________Creating Attribute Read Matrix_______________________
Arm_Matrix= [[0 for i in range(10)] for j in range(8)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if value is not 0:
            if type(value)is list:          #this list is data type list
                for i in value:
                    if i is 3:
                        Arm_Matrix[int(index/3)][Index_of_List]+=1
            else:
                if value is 3:
                     Arm_Matrix[int(index/3)][Index_of_List]+=1
            index+=1
        else:
            index+=1
    Index_of_List+=1

#print(Arm_Matrix)
#__________________________Now study Paper Well and do final stuff__________________
