from collections import defaultdict
import sys
from pprint import pprint as pp
#Creating and initialising ECRUD Matrix
Site=8 			#Total number of sites
Attribute=10 	#Total number of Attributes
ECRUD_Matrix=[['C','R','U','','','','','','','','','','','','','C','U','R','','','','','',''],
              ['','','','C',['C','R'],'D','','','',['R','U'],['C','U'],'D','','','','','','','','','','','',''],
              ['','','',['C','U','R'],'R','D','','','','','','','','','','','','',['U','D'],'R','R','R','R','U'],
              ['','','','','','','C','R','U','','','','','','','','','','','','','C','R','D'],
              ['U','R','D','','','','','','','','','','','','','R','R','U','','','','','',''],
              ['','','','','','','C','R','D','','','','','','','','','','','','','C','U','D'],
              ['U','D','R','','','','','','','C','U','D','','','','','','','','','','','',''],
              ['','','','C','R','D','','','','D','D','R','','','','','','','','','','','',''],
              ['','','','C','R','D','','','','','','','','','','','','',['C','U','R'],['C','U','R'],'R','R','R','D'],
              ['','','','','','','C','R','U','','','','','','','','','','','','','C','R','D']]
			  
#________________________Creating Attribute Site Usage Matrix____________________________
Asum_Matrix = [[0 for i in range(8)] for j in range(10)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if index%3 is not 0: #Here we are taking 3 applications in each site
            index+=1
            continue
        if value!='':
            Asum_Matrix[Index_of_List][int(index/3)]=1
            index+=1
        else:
            index+=1
    Index_of_List+=1
#print(Asum_Matrix)

#_________________________Creating Attribute Similarity Matrix__________________________
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

			
#print(Asm_matrix)

#_________________________Now Constructing Spanning tree On Asm_Matrix____________________________

edges=[]
class Heap():

	def __init__(self):
		self.array = []
		self.size = 0
		self.pos = []

	def newMaxHeapNode(self, v, dist):
		maxHeapNode = [v, dist]
		return maxHeapNode

	# A function to swap two nodes of max heap. Needed for max heapify
	def swapMaxHeapNode(self,a, b):
		t = self.array[a]
		self.array[a] = self.array[b]
		self.array[b] = t

	# A function to heapify.
	# This function also updates position of nodes when they are swapped. Position is needed for decreaseKey()
	def maxHeapify(self, idx):
		largest = idx
		left = 2*idx + 1
		right = 2*idx + 2

		if left < self.size and self.array[left][1] > self.array[largest][1]:
			largest = left

		if right < self.size and self.array[right][1] > self.array[largest][1]:
			largest = right

		# The nodes to be swapped in max heap if idx is not largest
		if largest != idx:

			# Swap positions
			self.pos[ self.array[largest][0] ] = idx
			self.pos[ self.array[idx][0] ] = largest

			# Swap nodes
			self.swapMaxHeapNode(largest, idx)

			self.maxHeapify(largest)

	# Standard function to extract maximum node from heap
	def extractMax(self):

		# Return NULL if heap is empty
		if self.isEmpty() == True:
			return

		# Store the root node
		root = self.array[0]

		# Replace root node with last node
		lastNode = self.array[self.size - 1]
		self.array[0] = lastNode

		# Update position of last node
		self.pos[lastNode[0]] = 0
		self.pos[root[0]] = self.size - 1

		# Reduce heap size and heapify root
		self.size -= 1
		self.maxHeapify(0)

		return root

	def isEmpty(self):
		return True if self.size == 0 else False

	def decreaseKey(self, v, dist):
		i = self.pos[v]
		self.array[i][1] = dist

		# Travel up while the complete tree is not heapified. This is a O(Logn) loop
		while i > 0 and self.array[i][1] > self.array[int((i-1)/2)][1]:

			# Swap this node with its parent
			self.pos[ self.array[i][0] ] = int((i-1)/2)
			self.pos[ self.array[int((i-1)/2)][0] ] = i
			self.swapMaxHeapNode(i, int((i - 1)/2) )

			# move to parent index
			i = int((i - 1) / 2);

	# A function to check if a given vertex 'v' is in max heap or not
	def isInMaxHeap(self, v):

		if self.pos[v] < self.size:
			return True
		return False


def printArr(parent, n):
	for i in range(1,n):
		edges.append((parent[i], i))
		print ("%d - %d" % (parent[i], i))


class Graph():

	def __init__(self, V):
		self.V = V
		self.graph = defaultdict(list)

	# Adds an edge to an undirected graph
	def addEdge(self, src, dest, weight):

		# Add an edge from src to dest. 
		newNode = [dest, weight]
		self.graph[src].insert(0, newNode)

		# Since graph is undirected, add an edge from dest to src also
		newNode = [src, weight]
		self.graph[dest].insert(0, newNode)

	# The main function 
	# It is a O(ELogV) function
	def PrimMST(self):
		V = self.V 
		# key values used to pick maximum weight edge in cut
		key = [] 
		# List to store contructed MST
		parent = [] 
		# maxHeap represents set E
		maxHeap = Heap()
		# Initialize max heap with all vertices. Key values of all vertices (except the 0th vertex) is initially 0
		for v in range(V):
			parent.append(-1)
			key.append(0)
			maxHeap.array.append( maxHeap.newMaxHeapNode(v, key[v]) )
			maxHeap.pos.append(v)

		# Make key value of 0th vertex as -1 so that it is extracted first
		maxHeap.pos[0] = 0
		key[0] = -1
		maxHeap.decreaseKey(0, key[0])
		# Initially size of max heap is equal to V
		maxHeap.size = V;
		
		while maxHeap.isEmpty() == False:
			# Extract the vertex with maximum distance value
			newHeapNode = maxHeap.extractMax()
			u = newHeapNode[0]
			# Traverse through all adjacent vertices of u (the extracted vertex) and update their distance values
			for pCrawl in self.graph[u]:
				v = pCrawl[0]
				if maxHeap.isInMaxHeap(v) and pCrawl[1] > key[v]:
					key[v] = pCrawl[1]
					parent[v] = u
					# update distance value in max heap also
					maxHeap.decreaseKey(v, key[v])
		printArr(parent,V)


#__________________________________________creating graph_________________________________________
graph = Graph(10)
for i in range(10):
	for j in range(10):
			graph.addEdge(j,i ,Asm_matrix[j][i] )

graph.PrimMST()

#_______________________________________partitioning__________________________________________
class DisjointSet(object):

    def __init__(self):
        self.leader = {} # maps a member to the group's leader
        self.group = {} # maps a group leader to the group (which is a set)

    def add(self, a, b):
        leadera = self.leader.get(a)
        leaderb = self.leader.get(b)
        if leadera is not None:
            if leaderb is not None:
                if leadera == leaderb: return 
                groupa = self.group[leadera]
                groupb = self.group[leaderb]
                if len(groupa) < len(groupb):
                    a, leadera, groupa, b, leaderb, groupb = b, leaderb, groupb, a, leadera, groupa
                groupa |= groupb
                del self.group[leaderb]
                for k in groupb:
                    self.leader[k] = leadera
            else:
                self.group[leadera].add(b)
                self.leader[b] = leadera
        else:
            if leaderb is not None:
                self.group[leaderb].add(a)
                self.leader[a] = leaderb
            else:
                self.leader[a] = self.leader[b] = a
                self.group[a] = set([a, b])

ds = DisjointSet()
k=2 #Number of Cluster
#k=int(input('Enter value for K : '))
for i in range(k-1):
	min=sys.maxsize
	for v1,v2 in edges:
		if(min>Asm_matrix[v1][v2]):
			min=Asm_matrix[v1][v2]
			del_v1,del_v2=v1,v2
	edges.remove((del_v1,del_v2))
print(edges)
for x,y in edges:
    ds.add(x, y)
#pp(ds.group)

#Node_in_ST_WithRoot contains info in the form of {node:root}
#Node_distnace_lis contains info in the form of {key:{distance:d,root:r}}
#which tells node 'key' is at distance d from node 'r'

#______________________Creating Attribute Manipulate Matrix_______________________
Amm_Matrix= [[0 for i in range(10)] for j in range(8)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if value != '':
            if type(value)is list:          #this list is data type list
                for i in value:
                    if i is 'C' or i is 'U' or i is 'D':
                        Amm_Matrix[int(index/3)][Index_of_List]+=1
            else:
                if value is 'C' or value is 'U' or value is 'D':
                     Amm_Matrix[int(index/3)][Index_of_List]+=1
            index+=1
        else:
            index+=1
    Index_of_List+=1
#print("Attribute Manipulate Matrix : ")
#print(Amm_Matrix)
#______________________________Creating Attribute Read Matrix_______________________
Arm_Matrix= [[0 for i in range(10)] for j in range(8)]
Index_of_List=0
for lis in ECRUD_Matrix:
    index=0
    for value in lis:
        if value != '':
            if type(value)is list:          #this list is data type list
                for i in value:
                    if i is 'R':
                        Arm_Matrix[int(index/3)][Index_of_List]+=1
            else:
                if value is 'R':
                     Arm_Matrix[int(index/3)][Index_of_List]+=1
            index+=1
        else:
            index+=1
    Index_of_List+=1
#print("Attribute Read Matrix : ")
#print(Arm_Matrix)

#__________________________________Fragment Allocation and Replication________________________________
l=[]
manipulate_opr={}
read_opr={}
sum_m=0
sum_r=0
j=0
print("\n\n")
#initialising a list with edges
for i in ds.group.keys():
	l.append(ds.group[i])
	j=j+1
	print("Fragment:",j)
	print(ds.group[i])

print("\n\n")
#initialising the dictionary
for j in range(Site):
	manipulate_opr.update({j+1:[]})	
	read_opr.update({j+1:[]})
#Calculating number of manipulate operations and read operations of each site
for j in range(Site):
	for i in range(k):
		sum_m=0
		sum_r=0
		for m in l[i]:
			sum_m=sum_m+Amm_Matrix[j][m]
			sum_r=sum_r+Arm_Matrix[j][m]
		manipulate_opr[j+1].append(sum_m)	
		read_opr[j+1].append(sum_r)

print("Manipulate operations :")
print("Site".rjust(5),end="		")
for i in range(k):
	print(i+1,end="")
	print("Fragment".rjust(5),end="	")
print("\n")
for j in range(Site):
	v=j+1
	s=str(v)
	print(s.rjust(5),end="		")
	for i in range(k):
		v=manipulate_opr[j+1][i]
		s=str(v)
		print(s.rjust(5),end="		")
	print()
print("\n \n \n ")
print("Read operations :")
print("Site".rjust(5),end="		")
for i in range(k):
	print(i+1,end="")
	print("Fragment".rjust(5),end="	")
print("\n")
for j in range(Site):
	v=j+1
	s=str(v)
	print(s.rjust(5),end="		")
	for i in range(k):
		v=read_opr[j+1][i]
		s=str(v)
		print(s.rjust(5),end="		")
	print()

#Allocation and replication of fragments
for i in range(k):
	max_m=manipulate_opr[1][i]
	max_m_key=1
	max_r=read_opr[1][i]
	max_r_key=1
	for j in range(2,Site+1):
		if max_m < manipulate_opr[j][i]:
			max_m=manipulate_opr[j][i]
			max_m_key=j
		if max_r < read_opr[j][i]:
			max_r=read_opr[j][i]
			max_r_key=j
	print("Fragment : ",i+1)
#replication of fragment should not be done to same site where allocation has been done
	if max_m_key == max_r_key:
		print("Allocation to site:",max_m_key)
		max_r=read_opr[1][i]
		similar_key=max_r_key
		max_r_key=1
		for k in range(2,Site+1):
			if max_r < read_opr[k][i] and k != similar_key: 
				max_r=read_opr[k][i] 
				max_r_key=k
		print("Replication to site:",max_r_key)
	
	else:
		print("Allocation to site:",max_m_key)
		print("Replication to site:",max_r_key)
	
	


	
	