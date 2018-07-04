
from random import randint

from BaseAI import BaseAI

from time import time

class PlayerAI(BaseAI):

    def timeIsUp(self,start_time):
        time_limit = 0.2
        return((time()-start_time)>=time_limit)


    def heuristic(self,grid):
        #For the heuristic, higher is better.
        free_cells = grid.getAvailableCells()
        return(len(free_cells))

    def Maximize(self, grid, depth, max_depth, start_time):

        if self.timeIsUp(start_time):
            print('out of time for this move')
            return(('timeout', None, self.heuristic(grid)))


        if depth>max_depth:
            return(('time remaining', None, self.heuristic(grid)))

        max_val = -10000000
        max_child = None
        moves = grid.getAvailableMoves()

        if len(moves)==0:
            return(('time remaining', None, self.heuristic(grid)))
        #print('\nMaximize at depth {} looking at moves {}'.format(depth,moves))
        for move in moves:
            temp_grid = grid.clone()
            temp_grid.move(move)
            (time_status, child, val) = self.Minimize(temp_grid,depth+1,max_depth, start_time)
            if time_status=='timeout':
                return('timeout',max_child,max_val)
            if val>max_val:
                max_val = val
                max_child = move


        return(('time remaining', max_child, max_val))


    def Minimize(self, grid, depth, max_depth, start_time):

        if self.timeIsUp(start_time):
            print('out of time for this move')
            return(('timeout', None, self.heuristic(grid)))

        if depth>max_depth:
            return(('time remaining', None, self.heuristic(grid)))

        min_val = 10000000
        min_child = None
        free_cells = grid.getAvailableCells()
        tiles = [(cell,2) for cell in free_cells]+[(cell,4) for cell in free_cells]

        if len(tiles)==0:
            return(('time remaining', None, self.heuristic(grid)))

        #print('\nMinimize at depth {} looking at tiles {}'.format(depth,tiles))
        for tile in tiles:
            temp_grid = grid.clone()
            temp_grid.insertTile(tile[0],tile[1])
            (time_status, child, val) = self.Maximize(temp_grid,depth+1,max_depth, start_time)
            if time_status=='timeout':
                return('timeout',min_child,min_val)
            if val<min_val:
                min_val = val
                min_child = tile


        return(('time remaining', min_child, min_val))



    def getMove(self, grid):

        start_time = time()

        best_val = -1000000
        best_move = None

        max_depth = 1
        time_status = 'time remaining'
        while time_status!='timeout':

            (time_status, best_move_at_depth, best_val_at_depth) = self.Maximize(grid,1,max_depth, start_time)
            print('best move and value at depth {}: {},{}'.format(max_depth,best_move_at_depth,best_val_at_depth))
            if best_val_at_depth>best_val:
                best_val = best_val_at_depth
                best_move = best_move_at_depth

            max_depth += 1

        print('best move:',best_move)
        print('best value:',best_val)
        return(best_move)













#
