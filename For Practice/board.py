

def valid_solution(board):
    
    # check if sum of all rows is 45

    for i in range(9):
        if sum(board[i]) != 45:
            return False

    # check if sum of all columns is 45

    for i in range(9):
        sum_c = 0
        for j in range(9):
            sum_c += board[j][i]
        if sum_c != 45:
            return False                

    # check if every 3x3 block is 45
    
    for a in range(0,9,3):
        sum_3 = 0
        for i in range(a,a+3):
            for j in range(a,a+3):
                sum_3 += board[j][i]
        if sum_3 != 45:
            print(sum_3)
            return False

    # if all pass, return True
    return True

print(valid_solution([
  [5, 3, 4, 6, 7, 8, 9, 1, 2],
  [6, 7, 2, 1, 9, 5, 3, 4, 8],
  [1, 9, 8, 3, 4, 2, 5, 6, 7],
  [8, 5, 9, 7, 6, 1, 4, 2, 3],
  [4, 2, 6, 8, 5, 3, 7, 9, 1],
  [7, 1, 3, 9, 2, 4, 8, 5, 6],
  [9, 6, 1, 5, 3, 7, 2, 8, 4],
  [2, 8, 7, 4, 1, 9, 6, 3, 5],
  [3, 4, 5, 2, 8, 6, 1, 7, 9]
]))
