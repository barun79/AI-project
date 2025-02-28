Name: Barun Singh
UTA_ID: 1002064749

Programming language used: Python

Code structure:
    Each search algorithmn is define using seperate function.
    Functions:
        file_to_array(filename): takes the txt file for the start and the goal state and convert the file into 2D file_to_array
        find_blank_position(array): finds the position of the 0 at a particular state and returns the row and column 
        valid_moves(row, column): This function provided the row and the column of the 0, gives the valid moves that can be made
        swap_state(array , row1, column1, row2, column2): this function swap the two values in an array provided the array and the two rows and columns
        moves_direction: It a graph that corresponds the coordinates with the direction
        moves_coorndiante: It is a graph that corresponds the direction with the coordinates
        visualization(start_array, path): This is a function to print the array provided the path just for the purpose of visualization
        manhatten_distance(start_array, final_array): This is a function to find the heuristic for the greedy and A* algorithms
        current_position(val , final_array): Helper function to find the manhatten distance which finds the current poisition of the value in the goal state
        main: It is the main function for the execution of the Code

Running the code:
    python expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>
            -<method> can be used with various commands
                    bfs - Breadth First Search
                    ucs - Uniform Cost Search
                    dfs - Depth First Search 
                    dls - Depth Limited Search
                    ids - Iterative Deepening Search 
                    greedy - 
                    a* - A* Search 

            - <dump-flag> optional
                If not provided default is false
                If provided true it will provide the trace file






