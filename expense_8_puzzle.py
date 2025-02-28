# Barun Singh
# 1002064749

import sys
import copy
import heapq
import datetime

def file_to_array(filename):
    with open(filename, "r") as file:
        array = []
        for line in file:
            line = line.strip()
            if line == "END OF FILE":
                break
            array.append([int(num)for num in line.split()])
        return array
    
def find_blank_position(array):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 0:
                return i , j  

def valid_moves(row, column):
    moves = []

    # Down move
    if row + 1 <= 2:
        moves.append((row+1, column))
    
    # Up move
    if row -1 >= 0:
        moves.append((row -1, column))

    #  Right move
    if column + 1 <= 2:
        moves.append((row, column + 1))
    
    if column -1 >= 0:
        moves.append((row, column -1))
    
    return moves

def swap_state(array , row1, column1, row2, column2):
    new_array = copy.deepcopy(array)
    temp = new_array[row1][column1]
    new_array[row1][column1] = new_array[row2][column2]
    new_array[row2][column2] = temp
    return new_array

moves_direction= {
    (1,0): "UP",
    (-1,0): "DOWN",
    (0,1): "LEFT",
    (0,-1): "RIGHT"
}

moves_coorndiante= {
    "UP": (1,0) ,
    "DOWN":(-1,0),
    "LEFT":(0,1),
    "RIGHT":(0,-1)
}

def visualization(start_array, path):
    new_array = copy.deepcopy(start_array)
    print("Start Puzzle:")
    for j in new_array:
        print(j)
    print()

    for move in path:
        direction = move.split()
        row_change , column_change = moves_coorndiante[direction[-1]]
        row , column = find_blank_position(new_array)
        new_array = swap_state(new_array,row_change + row, column_change+column,row, column)
        print(move, " :")
        for j in new_array:
            print(j)
        print()

def bfs_search(start_array,final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    queue = []
    queue.append([start_array, [], [], 0])
    visited = set()
    if tracefile:
        tracefile.write(f"Running bfs\n")

    while len(queue)!= 0:
        processing = queue.pop(0)
        nodes_popped +=1
        current_state , action , parent , cost = processing[0] , processing[1], processing[2], processing[3]
        if current_state == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution found at depth {len(action)} with the cost {cost}")
            return action
        if tuple(map(tuple,current_state)) not in visited:
            nodes_expanded += 1
            visited.add(tuple(map(tuple,current_state)))
            row , column = find_blank_position(current_state)
            moves = valid_moves(row , column)
            if tracefile:
                tracefile.write(f"Generating succesors to < state = {current_state}, action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")

            for move in moves:
                nodes_generated +=1
                new_array = swap_state(current_state, row, column, move[0], move[1])
                move_name = moves_direction[(move[0] - row, move[1]-column)]
                new_action = action + ["MOVE "+ str(new_array[row][column])+ " "+ move_name]
                new_cost = cost + new_array[row][column]
                if new_array == final_array:
                    print(f"Nodes Popped: {nodes_popped}")
                    print(f"Nodes Expanded: {nodes_expanded}")
                    print(f"Nodes Generated: {nodes_generated}")
                    print(f"Max Fringe Size: {max_fringe_size}")
                    print(f"Solution found at depth {len(new_action)} with the cost {new_cost}")
                    return new_action
                queue.append([new_array , new_action, processing, new_cost])
            
            if max_fringe_size < len(queue):
                max_fringe_size = len(queue)
            if tracefile:
                for array in queue:
                    tracefile.write(f"\t \t < state = {array[0]} , action = {array[1]}, parent = {array[2]} \n")
                tracefile.write("\t ] \n")
            
    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None     

def uniform_search(start_array, final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    queue = []
    heapq.heappush(queue,(0,start_array,[],[]))
    visited = {}
    if tracefile:
        tracefile.write(f"Running Uniform cost Search\n")

    while queue:
        processing = heapq.heappop(queue)
        cost , array , action, parent = processing[0], processing[1], processing[2], processing[3]
        nodes_popped +=1

        if array == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution found at depth {len(action)} with the cost of {cost}")
            return action
        
        processing = tuple(map(tuple, array))

        if processing not in visited or visited[processing] > cost:
            nodes_expanded += 1
            visited[processing] = cost
            row , column = find_blank_position(array)
            moves = valid_moves(row, column)
            if tracefile:
                tracefile.write(f"Generating succesors to < state = {array}, cost = {cost},  action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")
            
            for move in moves:
                nodes_generated +=1
                new_array = swap_state(array,move[0], move[1], row, column)
                moves_name ="MOVE " + str(new_array[row][column]) + " " +  moves_direction[(move[0] - row, move[1]-column)]
                heapq.heappush(queue,(cost + new_array[row][column],new_array, action + [moves_name], processing))
            if max_fringe_size < len(queue):
                max_fringe_size = len(queue)

            if tracefile:
                for array in queue:
                    tracefile.write(f"\t \t < state = {array[0]} , cost = {array[1]} action = {array[2]}, parent = {array[3]} \n")
                tracefile.write("\t ] \n")
    
    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def manhatten_distance(start_array, final_array):
    total_distance = 0
    for i in range(len(start_array)):
        for j in range(len(start_array[0])):
            k , l = current_position(start_array[i][j],final_array)
            total_distance += abs(i-k)+abs(j-l)
    return total_distance

def current_position(val , final_array):
    for i in range(len(final_array)):
        for j in range(len(final_array[0])):
            if final_array[i][j] == val:
                return i , j

def greedy_search(start_array, final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    queue = []
    heapq.heappush(queue, (manhatten_distance(start_array, final_array), 0 , start_array, [], []))
    visited = set()
    if tracefile:
        tracefile.write(f"Running Greedy Search\n")

    while queue:
        nodes_popped +=1
        processing = heapq.heappop(queue)
        heuristic, cost, array , action, parent = processing[0] , processing[1] , processing[2] , processing[3], processing[4]
        tuple_array = tuple(map(tuple, array))

        if array == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution found at depth {len(action)} with the cost of {cost}")
            return action
        
        if tuple_array not in visited:
            nodes_expanded += 1
            visited.add(tuple_array)

            row , column = find_blank_position(array)
            moves = valid_moves(row, column)

            if tracefile:
                tracefile.write(f"Generating succesors to < state = {array}, cost = {cost},  action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")

            for move in moves:
                nodes_generated +=1
                new_array = swap_state(array, row , column , move[0], move[1])
                move_name = moves_direction[(move[0] - row, move[1] - column)]
                heapq.heappush(queue, (manhatten_distance(new_array, final_array), cost + new_array[row][column], new_array, action + ["MOVE " + str(new_array[row][column])+" "+move_name],processing))
            
            if max_fringe_size < len(queue):
                max_fringe_size = len(queue)
            
            if tracefile:
                for array in queue:
                    tracefile.write(f"\t \t < state = {array[0]} , cost = {array[1]} action = {array[2]}, parent = {array[3]} \n")
                tracefile.write("\t ] \n")

    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def a_star(start_array, final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    queue = []
    heapq.heappush(queue,(manhatten_distance(start_array, final_array), 0, start_array, [], []))
    visited = {}
    if tracefile:
        tracefile.write(f"Running A* Search\n")

    while queue:
        nodes_popped +=1
        processing = heapq.heappop(queue)
        f_cost, g_cost , array, action , parent = processing[0], processing[1], processing[2], processing[3], processing[4] 
        tuple_array = tuple(map(tuple, array))

        if array == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution found at depth {len(action)} with the cost of {g_cost}")
            return action

        if tuple_array not in visited or visited[tuple_array] > g_cost:
            nodes_expanded += 1
            visited[tuple_array] = g_cost

            row , column = find_blank_position(array)
            moves = valid_moves(row, column)
            if tracefile:
                tracefile.write(f"Generating succesors to < state = {array}, cost = {f_cost},  action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")

            for move in moves:
                nodes_generated +=1
                new_array = swap_state(array,row , column , move[0], move[1])
                move_name = moves_direction[(move[0]-row, move[1]-column)]
                new_g_cost = g_cost + new_array[row][column]
                new_f_cost = new_g_cost + manhatten_distance(new_array, final_array)
                heapq.heappush(queue,(new_f_cost, new_g_cost, new_array, action + ["MOVE "+ str(new_array[row][column])+ " "+move_name], processing))
            
            if max_fringe_size < len(queue):
                max_fringe_size = len(queue)

            if tracefile:
                for array in queue:
                    tracefile.write(f"\t \t < state = {array[0]} , cost = {array[1]} action = {array[2]}, parent = {array[3]} \n")
                tracefile.write("\t ] \n")

    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def dfs_search(start_array,final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    stack = []
    stack.append([start_array, [], [], 0])
    visited = set()
    if tracefile:
        tracefile.write(f"Running Dfs\n")

    while len(stack)!= 0:
        processing = stack.pop()
        nodes_popped +=1
        current_state , action , parent, cost = processing[0] , processing[1], processing[2], processing[3]
        if current_state == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution was found at depth {len(action)} with the cost of {cost}")
            return action
        if tuple(map(tuple,current_state)) not in visited:
            nodes_expanded += 1
            visited.add(tuple(map(tuple,current_state)))
            row , column = find_blank_position(current_state)
            moves = valid_moves(row , column)
            if tracefile:
                tracefile.write(f"Generating succesors to < state = {current_state}, action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")

            for move in moves:
                nodes_generated +=1
                new_array = swap_state(current_state, row, column, move[0], move[1])
                move_name = moves_direction[(move[0] - row, move[1]-column)]
                new_action = action + ["MOVE "+ str(new_array[row][column])+ " "+ move_name]
                stack.append([new_array , new_action, processing, cost + new_array[row][column]])
            
            if max_fringe_size < len(stack):
                max_fringe_size = len(stack)
            if tracefile:
                for array in stack:
                    tracefile.write(f"\t \t < state = {array[0]} , action = {array[1]}, parent = {array[2]} \n")
                tracefile.write("\t ] \n")
            
    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def dls_search(start_array,final_array, depth_limit, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    stack = []
    stack.append([start_array, [], [],0, 0])
    if tracefile:
        tracefile.write(f"Running Dls\n")

    while stack:
        visited = set() 
        processing = stack.pop()
        nodes_popped +=1
        current_state , action , parent, depth, cost = processing[0] , processing[1], processing[2], processing[3], processing[4]
        if current_state == final_array:
            print(f"Nodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Max Fringe Size: {max_fringe_size}")
            print(f"Solution found at depth {len(action)} with the cost of {cost}")
            return action
        if depth < depth_limit:
            nodes_expanded += 1
            visited.add(tuple(map(tuple,current_state)))
            row , column = find_blank_position(current_state)
            moves = valid_moves(row , column)
            if tracefile:
                tracefile.write(f"Generating succesors to < state = {current_state}, action = {action}, parent = {parent}\n")
                tracefile.write(f"\t {len(moves)} successors generated\n")
                tracefile.write(f"\t Closed: {visited}\n")
                tracefile.write("\t Fringe: [\n")

            for move in moves:
                nodes_generated +=1
                new_array = swap_state(current_state, row, column, move[0], move[1])
                move_name = moves_direction[(move[0] - row, move[1]-column)]
                new_action = action + ["MOVE "+ str(new_array[row][column])+ " "+ move_name]
                stack.append([new_array , new_action, processing, depth+1, cost+ new_array[row][column]])
            
            if max_fringe_size < len(stack):
                max_fringe_size = len(stack)
            if tracefile:
                for array in stack:
                    tracefile.write(f"\t \t < state = {array[0]} , action = {array[1]}, parent = {array[2]} \n")
                tracefile.write("\t ] \n")
            
    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def ids_search(start_array,final_array, tracefile):
    nodes_popped = 0
    nodes_expanded = 0
    nodes_generated = 0
    max_fringe_size = 0
    depth_limit = 1
    stack = []
    
    if tracefile:
        tracefile.write(f"Running Ids\n")
    while True:
        stack.append([start_array, [], [],0, 0])
        visited = set()
        
        while stack:
            processing = stack.pop()
            nodes_popped +=1
            current_state , action , parent, depth, cost = processing[0] , processing[1], processing[2], processing[3], processing[4]
            if current_state == final_array:
                print(f"Nodes Popped: {nodes_popped}")
                print(f"Nodes Expanded: {nodes_expanded}")
                print(f"Nodes Generated: {nodes_generated}")
                print(f"Max Fringe Size: {max_fringe_size}")
                print(f"Solution was found at depth {len(action)} with the cost of {cost}")
                return action
            if depth < depth_limit:
                nodes_expanded += 1
                visited.add(tuple(map(tuple,current_state)))
                row , column = find_blank_position(current_state)
                moves = valid_moves(row , column)
                if tracefile:
                    tracefile.write(f"Generating succesors to < state = {current_state}, action = {action}, parent = {parent}\n")
                    tracefile.write(f"\t {len(moves)} successors generated\n")
                    tracefile.write(f"\t Closed: {visited}\n")
                    tracefile.write("\t Fringe: [\n")

                for move in moves:
                    nodes_generated +=1
                    new_array = swap_state(current_state, row, column, move[0], move[1])
                    move_name = moves_direction[(move[0] - row, move[1]-column)]
                    new_action = action + ["MOVE "+ str(new_array[row][column])+ " "+ move_name]
                    stack.append([new_array , new_action, processing, depth+1, cost+new_array[row][column]])
                
                if max_fringe_size < len(stack):
                    max_fringe_size = len(stack)
                if tracefile:
                    for array in stack:
                        tracefile.write(f"\t \t < state = {array[0]} , action = {array[1]}, parent = {array[2]} \n")
                    tracefile.write("\t ] \n")

        depth_limit +=1

    print(f"Nodes Popped: {nodes_popped}")
    print(f"Nodes Expanded: {nodes_expanded}")
    print(f"Nodes Generated: {nodes_generated}")
    print(f"Max Fringe Size: {max_fringe_size}")
    return None

def main():

    if (len(sys.argv)) < 4 or len(sys.argv) > 5:
        print("Usuage: python python_script.py start_file.txt goal_file.txt method")
        return

    start_array = file_to_array(sys.argv[1])
    final_array = file_to_array(sys.argv[2])
    search_algorithmn = sys.argv[3].upper()
    if len(sys.argv) == 5:
        dump_flag = sys.argv[4].lower()
    else:
        dump_flag = "false"
    
    trace_file = None
    if dump_flag == "true":
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        trace_filename = f"trace-{time}.txt"
        trace_file = open(trace_filename, "w")
        trace_file.write(f"Command_line Arguments : {sys.argv}\n")
        trace_file.write(f"Method selected: {sys.argv[3]}\n")
        

    if search_algorithmn == "BFS":
        print("Breadth First Search Algorithmns: ")
        path = bfs_search(start_array, final_array, trace_file)
    elif search_algorithmn == "UCS":
        print("Uniform Cost Search Algorithmns: ")
        path = uniform_search(start_array, final_array, trace_file)
    elif search_algorithmn == "GREEDY":
        print("Greedy Search Algorithmns: ")
        path = greedy_search(start_array, final_array, trace_file)
    elif search_algorithmn == "A*":
        print("A* search Alogithmns:")
        path = a_star(start_array, final_array,trace_file)
    elif search_algorithmn == "DFS":
        print("Depth First Search Algorithmns: ")
        path = dfs_search(start_array, final_array, trace_file)
    elif search_algorithmn == "DLS":
        print("Depth Limit Search Algorithmns: ")
        limit = int(input("Enter depth limit: "))
        path = dls_search(start_array, final_array, limit ,trace_file)
    elif search_algorithmn == "IDS":
        print("Iteratively Depeening Search Algorithmns: ")
        path = ids_search(start_array, final_array,trace_file)
    
    if trace_file:
        trace_file.close()
    
    if path:
        visualization(start_array, path)
    else:
        print("Solution could not be found")

if __name__ == "__main__":
    main()   