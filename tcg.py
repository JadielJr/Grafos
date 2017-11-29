V_ENABLE = 1
V_DISABLE = 0

class Vertex(object):
	def __init__(self):
		self.id = 0
		self.color = None
		self.status = V_ENABLE
		self.degree = 0
		self.label = ""			
		self.neighbors = []		#Adjacents vertices
		self.ecNumber = 0 		#not being used for now
		self.brand = V_ENABLE	#it may be that you participate in a motif
		self.level = 0			#discovery time of DFS 
		self.successors = []
		self.value = 1

	def printNeighbors(self):
		print("%d  {"%(self.id), end="")
		for neighbor in self.neighbors:
			print("----> %d"%( neighbor.id), end=" ")

		print("}")	
	

	def isAdjacent(self, i):
		for x in self.neighbors:
			if x.id == i:
				return 1
		return 0	

	def printSuccessors(self):
		print(self.id, "|", self.value, "--> {", end=" ")
		for successor in self.successors:
			print("-->",successor.id, end=" ")	
		print("}")

class Graph(object):
	def __init__(self):
		self.n = 0	        # Number of vertices 
		self.ocurrences = 0 # Number of ocurrences
		self.maxN = 0		# Max number of vertices
		self.maxColor = 0	# Max number of colors
		self.vList = []		# List of vertices
		self.topologicalSort = []
		self.level = 0

		self.map = []
	def printVertices(self):
		for vertex in self.vList:
			print(vertex.id, vertex.color, vertex.label)	
	
	def printAdjacents(self):
		for vertex in self.vList:
			vertex.printNeighbors()	

	#creates a graph referring to the input file		
	def CreateMotif(self, archive):
		arc = open(archive, 'r')
		entry = arc.readline()
		numberVertices, maxColor = entry.split(',')
		self.maxN = int(numberVertices)
		self.maxColor = int(maxColor)

		for i in range(self.maxN):
			line = arc.readline()
			index, color = line.split(':')
			vertex = Vertex()
			vertex.id = int(index)
			vertex.color = int(color)
			self.vList.append(vertex)
			self.n += 1
		
		lines = arc.readlines()
		
		for line in lines:
			index, neighbor = line.split('-')

			#Adding Edges between the vertices
			self.vList[int(index)].neighbors.append(self.vList[int(neighbor)])
			self.vList[int(neighbor)].neighbors.append(self.vList[int(index)])	
		arc.close()	
	#A Simple depth-first search
	def dfs(self):
		for vertex in self.vList:
			vertex.status = V_ENABLE
		
		for vertex in self.vList:
			if(vertex.status):
				self.dfsVisit(vertex)

	#2 step of depth-first search	
	def dfsVisit(self, vertex):
		vertex.status = V_DISABLE
	
		for neighbor in vertex.neighbors:
			if(neighbor.status):
				vertex.successors.append(neighbor)
				self.dfsVisit(neighbor)

		vertex.level = self.level		
		self.level +=1
		self.topologicalSort.append(vertex)

	#search for an instance of the motif in the graph
	def TCG(self, motif):
		for i in range(len(motif.topologicalSort)):
			v = motif.topologicalSort[i]
			A = []
			w = None
			
			for a in self.vList:
				if a.status == V_ENABLE and a.color == v.color:
					A.append(a)
			
			w = v.neighbors[0]

			#selecting neighbor that has a level greater than vertex v to maintain the order of dfs.
			for neighbor in v.neighbors:
				if(neighbor.level > v.level):	
					w = neighbor
					break
			

			if(i == len(motif.topologicalSort)-1):
				self.map.append(v)
				if(len(A) == 0):
					print("No occurrences")
					return;
				else:
					print("The motif occurs in the graph")
					return;	

			self.map.append(w)
		
			for b in self.vList:
				if b.status == V_ENABLE and b.color == w.color:
					if self.adjTo(b,v) == 1:
						self.vList[b.id].brand = V_DISABLE
						self.vList[b.id].status = V_DISABLE

			for a in self.vList:
				if a.status == V_ENABLE and a.color == v.color:
					self.vList[a.id].status = V_DISABLE			
	#It says if two vertices are adjacent
	def adjTo(self, x, w):
		for vertex in x.neighbors:
			if(vertex.status == 1 and vertex.color == w.color):
				return 0
		return 1	

	def ocurrence(self, array, motif):
		aux = self.map[-1]

		#Obtaining leaf belonging to a motif
		for v in self.vList:
			if v.brand == V_ENABLE and v.color == aux.color:
				#Adding vertex on ultimate position of array.
				array[-1] = v
				break
		for i in range(len(self.map)-2, -1, -1):
			
			index =  self.map[i].level
			
			vertex = array[index]
			color = motif.topologicalSort[i].color
			
			
			for neighbor in vertex.neighbors:
				if neighbor.brand == V_ENABLE and neighbor.color == color:
					array[i] = neighbor
					break	

		#Print the ocurrence
		print("Ocurrence:", end="")
		for i in range(0, len(array), 1):
			print(array[i].id, end=" ")
						

	def proxSeq(self, l, n):
	    i = len (l) - 1
	    x = n - 1
	    while i >= 0 and l[i] == x: 
	       i -= 1
	       x -= 1
	    if i == -1: return 0
	    x = l[i] + 1
	    while i < len(l):
	   	   l[i] = x
	   	   x += 1
	   	   i += 1
	    return 1

	def subsets(self, l, n):
		while(self.proxSeq(l,n)== 1):
			for i in range(1, len(l), 1):
				if not self.vList[l[0]].isAdjacent(l[i]):
					print(self.vList[l[0]].id, l[i])
					#Adding edges in the vertex 
					self.vList[l[0]].neighbors.append(self.vList[l[i]])
					self.vList[l[i]].neighbors.append(self.vList[0])
			
			print("")	
	


	def printSuccessors(self):
		for vertex in self.vList:
			print("Vertice => ", vertex.id, "Value =>", vertex.value, "-> {", end=" ")
			for successor in vertex.successors:
				print(successor.id, end=" ")
			print("}")	

	def countOcurrences(self, motif):
		for m in motif.topologicalSort:
			for v in self.vList:
				if v.color == m.color:
					countSuccessorM = 0
					countSuccessorV = 0
					count = 1
					for successor in m.successors:
						adder = 0
						countSuccessorM +=1
						flag = False
						
						for neighbor in v.neighbors:
							if neighbor.color == successor.color:
								v.successors.append(neighbor)
								adder+= neighbor.value
								flag = True
						if flag:
							countSuccessorV +=1

						count *= adder		
					
					if countSuccessorM == countSuccessorV:
						v.value = count
					else:
						v.value = 0														
					v.printSuccessors()
		color = motif.topologicalSort[-1].color
		result = 0
		for vertex in self.vList:
			if vertex.color == color:
				result+= vertex.value
		print("Total Ocurrences: ", result)		
						
							
#Initializing graph that be populated.
graph = Graph()	

#Open archive reference to graph
arq = open('graph-e.coli_BioCyc_K12-clean.txt', 'r')

#reading number of vertices and number maxime of colors
firstLine = arq.readline()

verticesNumber, colorsNumber = firstLine.split(',')
graph.maxN = int(verticesNumber)
graph.maxColor = int(colorsNumber)

#Initializing vertices
for i in range(graph.maxN):
	line = arq.readline()
	string1, string2 = line.split()
	index, color = string1.split(':')
	label, ec = string2.split(':')

	vertex = Vertex()
	vertex.id = int(index)
	vertex.color = int(color)
	vertex.label = label
	vertex.ecNumber = ec

	graph.vList.append(vertex)
	graph.n += 1

#Adding neighbors of the vertices
for line in arq.readlines():
	index, adj = line.split('-')
	
	graph.vList[int(index)].neighbors.append(graph.vList[int(adj)])
	graph.vList[int(adj)].neighbors.append(graph.vList[int(index)])


arq.close()

motif = Graph()

motif.CreateMotif("motif-600.txt")
'''
graph.subsets(list(range(2)), len(graph.vList))

motif.dfs()
print("Ordem topologica")
for x  in motif.topologicalSort:
	print(x.id, end=" - ")
print("\n------------------")
graph.TCG(motif)
	
#save an occurrence.
v = [None] * len(motif.vList)
graph.ocurrence(v, motif)
'''
motif.dfs()
graph.printAdjacents()
#motif.printSuccessors()
print("------------------------------")

graph.countOcurrences(motif)











