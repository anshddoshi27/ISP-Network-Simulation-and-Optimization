from graph import Graph, Vertex
from sys import maxsize
from priority_queue import PriorityQueue


class ISPNetwork:
    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    def buildGraph(self, filename: str) -> None:
        """
        loads data from file and assigns it to a graph instance that is in ISP Network's network attribute
         returns nothing
        :param filename: name of csv file with all link weights of a ISP netowrk // STRING
        """
        with open(filename,"r") as f: # open file
            for line in f: # loop through lines
                path=line.split(",") # each line turns to list of 3 items
                v1,v2,lw=path # assign elements in each line in file as vertex 1, vertex 2, and the link weight
                self.network.addEdge(str(v1),str(v2),int(lw)) # adds link of 2 routers and their link weight

    def pathExist(self, router1: str, router2: str, hops: int) -> bool:
        """
        function determines if there is a path between 2 given routers under a certain number of hops using BFS
        :param router1: vertex in network
        :param router2: vertex 2 that potentiall has a link to vertex 1
        :param hops: # limit of hops to check if there is possible path from routers 1 and 2
        :return: either TRUE or False if there is a path between 2 inputted routers
        """
        if not self.network.getVertex(router1) or not self.network.getVertex(router2): #checks if vertices exist in graph
            return False # if they aren't then returns false

        # BFS  method
        queue = [(router1, 0)]  # queue to keep track of ladder of vertices from start while counting hops
        visited = set()  # To keep track of visited routers, only UNIQUE routers disregarding quantities

        while queue: # while queue isn't empy
            current_router, current_hops = queue.pop(0)  # effectively Dequeue the next element or first element in list
            if current_router == router2 and current_hops <= hops: # if current router is router 2 then path exists
                return True # path exists so return TRUE

            if current_router in visited: # if the curretn_router has already been checked, we go to next iteration
                continue

            visited.add(current_router)  # if not already visited, it is visted now

            if current_hops < hops: # if hop limit not reached
                for neighbor in self.network.getVertex(current_router).getConnections(): # looping through all neighbors of current router vertex in ispnetwork graph
                    if neighbor.id not in visited: # if neighbor not already in queue
                        queue.append((neighbor.id, current_hops + 1)) # add neighbor to queue and add number of hops as ladder gets longer

        return False  # ladder extended to the end and current_router was never the same as router 2 so there is no possible path
    def buildMST(self, source) -> None:
        """
        creates a MST from isp network graph by creating a subgraph that connects a source or starting node to any
        other node in graph with smallest edge weight sum or cost of destination
        :param source:  vertex in isp network graph to start from when building MST or smallest path possible or smallest sum of weight possible
        :return: nothing, just creates MST, subgraph
        """
        start = self.network.getVertex(source) # starting vertex
        visited = set()  # Set of visited vertices
        pq = PriorityQueue()  # Priority queue for keeping track of the (weight, vertex)
        edge_map = {}  # Dictionary to track of edges by {vertex: weight, from_vertex}

        visited.add(start) # add starting node to visited
        for nbr in start.getConnections(): # loop through starting node's neighbors
            weight = start.getWeight(nbr) # assign weighto to the weigh of edge between start and neighbor
            pq.add((weight, nbr))  # Add the edge weight and neighbor vertex to priority queue
            edge_map[nbr] = (weight, start)  # add weight to dict of edges, key:node value: weight, node connected to (predecessor)

        # Construct the MST by adding minimum edges until all nodes are covered
        while not pq.isEmpty() and len(visited) < len(self.network.vertList): # mst is done when priority queue is empty and minimum vertices are covered
            min_vert = pq.delMin()  # Gets the vertex with the smallest weight

            # Retrieve the corresponding edge information from the edge_map
            if min_vert not in edge_map:
                continue  # skip if no edge stored for this vertex

            weight, from_vert = edge_map[min_vert] # weight of edge and other vertex becomes the minimum weighted vertex that has an edge with current vert

            # If the vertex is already in the MST, skip it
            if min_vert in visited: # if vertex already in visited we don't need to add it and we go to next itertion
                continue

            # Add the vertex and the edge to the MST
            visited.add(min_vert) # since none of other ocnditions were met we can safely add the minimum weighted vertex

            ## priority queue made so now mst ready to be formed from getting the min_verts
            if not self.MST.getVertex(from_vert.getId()): #if this vertex is start
                self.MST.addVertex(from_vert.getId()) # add vertex to mst
            if not self.MST.getVertex(min_vert.getId()): # if there's no vertex already in the mst that is mini_vert
                self.MST.addVertex(min_vert.getId()) # add the min vert to MST
            self.MST.addEdge(from_vert.getId(), min_vert.getId(), weight) # connect start and min_vert with an edge with its weight

            # Enqueue all neighbors of the min_vert that are not yet in the MST
            for nbr in min_vert.getConnections(): # loop through min_vert neighbors
                if nbr not in visited: # if nbr not visted
                    nbr_weight = min_vert.getWeight(nbr) # get weight of neighber
                    pq.add((nbr_weight, nbr))  # Add the new neighbor to the priority queue
                    # Update the edge_map to track the smallest edge to this neighbor
                    if nbr not in edge_map or nbr_weight < edge_map[nbr][0]: # if nbr not in edge map or neighber weight less than the first neighbor
                        edge_map[nbr] = (nbr_weight, min_vert)  # Update nbr to minivert

    def findPath(self, router1: str, router2: str) -> str:
        """
        find a path between 2 routhers using DFS, we are actually finding it in the MST
        :param router1: node 1
        :param router2: node 2
        :return: string of both routher key names with an arrow
        """
        # Check if both routers exist in the MST
        if not self.MST.getVertex(router1) or not self.MST.getVertex(router2):
            return "path not exist"

        # Helper function to find path between the rouuters thru dfs
        def dfs(current, target, visited, path):
            visited.add(current) # add current to visited
            path.append(current) # add current to the ladder or path

            # If we reached the target router, return the path
            if current == target: # if current is the target
                return True # router found

            #keep finding in all the current's neighbors
            for neighbor in self.MST.getVertex(current).getConnections(): # loop through current's neighbors
                if neighbor.getId() not in visited: # if neibor not in visiteed
                    if dfs(neighbor.getId(), target, visited, path):  # if path exists
                        return True

            # if path wasn't found, remove node
            path.pop()
            return False

        visited = set() # visited initialized
        path = [] # path initialized

# main codee
        if dfs(router1, router2, visited, path):
            # Return the path as a string with '->' separators
            return "->".join(path) # format so it shows routers connected
        else:
            return "path not exist" # if path dne

    def findForwardingPath(self, router1: str, router2: str) -> str:
        """
        Find the forwarding path between any two routers in the original network graph. To
        forward packets between any two routers, it’s better to use the path with minimal cost. Therefore,
        the forwarding path should ONLY consider the path with minimal cumulative cost, return
        the minimal cost as wel
        :param router1:
        :param router2:
        :return: shows both routers with an arrow
        """

        if not self.network.getVertex(router1) or not self.network.getVertex(router2):  # Check if both routers even exist in the network
            return "path not exist" # return it dosen't exist

        # Dijkstra's algorithm
        pq = PriorityQueue()  # Priority queue to store (cumulative cost, router)
        distances = {router: float('inf') for router in self.network.vertList}  # Initialize distances
        previous = {router: None for router in self.network.vertList}  # To reconstruct the path
        distances[router1] = 0  # Distance to the start router is 0
        pq.add((0, router1))  # Add starting router to the priority queue


        while not pq.isEmpty(): # While not empty
            current_router = pq.delMin()  # This returns the router with  minimum cost
            current_cost = distances[current_router]   # Get the router with the smallest  cost


            if current_router == router2: # if current is target
                path = [] # path inititalized to be reconstrcutedf
                while current_router is not None: #loop till all routers looped throu
                    path.insert(0, current_router) # insert current router at index 0
                    current_router = previous[current_router] # move current router to left
                return "->".join(path) + f" ({distances[router2]})" # return the path as a str

            current_vertex = self.network.getVertex(current_router)     # Get the current router vertex object


            for neighbor in current_vertex.getConnections():             # Loop through all the neighbors of the current router

                neighbor_id = neighbor.getId()  # Get the neighbor's ID
                edge_weight = current_vertex.getWeight(neighbor)  # Get the edge weight between current and neighbor
                new_cost = current_cost + edge_weight  # Calculate the new cumulative cost to this neighbor

                if new_cost < distances[neighbor_id]:                 # If the new cost is less than the previously known cost, update the distance
                    distances[neighbor_id] = new_cost  # Update the shortest distance
                    previous[neighbor_id] = current_router  # Record the path
                    pq.add((new_cost, neighbor_id))  # Add the neighbor to the priority queue with the updated cost

        return "path not exist" # if queue all searched and path not found

    def findPathMaxWeight(self, router1: str, router2: str) -> str:
        """
        to find the path between two routers based on max link weight based on diagrma as well
        :param router1: ndoe 1
        :param router2:node 2
        :return: path between 2 strings with arrow as a str
        """
        if not self.network.getVertex(router1) or not self.network.getVertex(router2):         # Check if both routers exist in the network
            return "path not exist"

        pq = PriorityQueue()         # Initialize priority queue and tracking dictionaries
        max_weights = {router: float('inf') for router in self.network.vertList}  # Max weight along path to router
        previous = {router: None for router in self.network.vertList}  # To reconstruct the path
        max_weights[router1] = 0  # The max weight along the path to the start router is 0
        pq.add((0, router1))  # Add the starting router with a max weight of 0

        while not pq.isEmpty():    # While the priority queue is not empty
            current_router = pq.delMin()             # Get the router with the smallest maximum link weight encountered so far
            current_max_weight = max_weights[current_router]  # Get its max weight from the dictionary
            if current_router == router2:             # If we reached the destination router, reconstruct the path
                path = [] # path initialized
                while current_router is not None: # while all rout not found
                    path.insert(0, current_router) #insert  current at 0
                    current_router = previous[current_router] #move current to the left
                return "->".join(path) # reutn the str

            current_vertex = self.network.getVertex(current_router)   # Get the current router vertex object


            for neighbor in current_vertex.getConnections():             # Loop through all the neighbors of the current router
                neighbor_id = neighbor.getId() # get name
                edge_weight = current_vertex.getWeight(neighbor) # get weight
                new_max_weight = max(current_max_weight, edge_weight)  # Calculate the new max weight

                if new_max_weight < max_weights[neighbor_id]:                 # If this path gives a smaller max weight, update the dictionaries
                    max_weights[neighbor_id] = new_max_weight # assign to new max weight
                    previous[neighbor_id] = current_router  # Record  path
                    pq.add((new_max_weight, neighbor_id))  # Add  neighbor with the updated max weight

        return "path not exist"         # If we exhaust the queue and don't find router2, return "path not exist"

    def checkLoop(self, destination: str = None, route: dict[str, str] = None) -> bool:
        if destination is None: #  case where 'destination'not  provided
            raise ValueError("Destination router must be provided.")
        if not route:        #  case where 'route' is not provided or is empty
            return False  # No route means no loop is possible

        visited = set()  # track routers that are visited, unqiue again
        current_router = destination  # Start from the given destination router

        while current_router in route:         # Follow the route chain until we either find a loop or run out of next hops
            if current_router in visited:  # Loop detected, revisiting a router
                return True # return true if detected
            visited.add(current_router)  # Mark this router as visited
            current_router = route[current_router]  # Move to the next hop router

        return False         # If we exit the while loop without revisiting any router, there's no loop

