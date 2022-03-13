#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import random
import copy

import os

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    GameStatus : this data include all field status, 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : this data include next shape position and the other,
    #               if return None, do nothing to nextMove.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # get data from GameStatus
        # current shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        # next shape info
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000
        # search with current block Shape
        for direction0 in CurrentShapeDirectionRange:
            # search with x range
            x0Min, x0Max = self.getSearchXRange(self.CurrentShape_class, direction0)
            for x0 in range(x0Min, x0Max):
                # get board data, as if dropdown block
                board = self.getBoard(self.board_backboard, self.CurrentShape_class, direction0, x0)

                ## evaluate board
                #EvalValue = self.calcEvaluationValueUSAMI(board)
                ## update best move
                #if EvalValue > LatestEvalValue:
                #    strategy = (direction0, x0, 1, 1)
                #    LatestEvalValue = EvalValue

                #1手先を読んで配置する
                for direction1 in NextShapeDirectionRange:  
                    x1Min, x1Max = self.getSearchXRange(self.NextShape_class, direction1)
                    for x1 in range(x1Min, x1Max):
                            board2 = self.getBoard(board, self.NextShape_class, direction1, x1)
                            EvalValue = self.calcEvaluationValueUSAMI(board2)
                            if EvalValue > LatestEvalValue:
                                strategy = (direction0, x0, 1, 1)
                                LatestEvalValue = EvalValue
        # search best nextMove <--

        print("===", datetime.now() - t1)
        nextMove["strategy"]["direction"] = strategy[0]
        nextMove["strategy"]["x"] = strategy[1]
        nextMove["strategy"]["y_operation"] = strategy[2]
        nextMove["strategy"]["y_moveblocknum"] = strategy[3]
        print(nextMove)
        print("###### USAMI CODE ######")
        
        return nextMove
        
    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValueUSAMI(self, board):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## 複数列消しフラグ
        hasMaxfullLines = False
        has3fullLines = False
        has2fullLines = False
        ## リーチ状態のline数
        reachlines = 0
        ## Blockが横に8つ並んでいる(セミリーチ)line数
        w8lines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
<<<<<<< HEAD
        #浮いているブロックの数
        nFloatingBlocks = 0

=======
        # 上がふさがった穴の数
        nDeadHoles = 0
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
        ## absolute differencial value of MaxY
        absDy = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width
<<<<<<< HEAD
        ## 上がふさがっているFloatingBlock の候補と確定
        FloatingBlockCandidates = [0] * width
        FloatingBlockConfirm = [0] * width
        #y列目ごとにあるブロックの数
        nBlocksEachLine = [0] * height
        #y列目ごとにある浮いているブロックの数
        nFloatingBlocksEachLine = [0] * height
=======
        ## 上がふさがっているDeadhole の候補と確定
        deadholeCandidates = [0] * width
        deadholeConfirm = [0] * width
        #y列目ごとにあるブロックの数
        nBlocks = [0] * height

>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            hasReach = False
<<<<<<< HEAD
            hasFloatingBlock = False
            
=======
            hasDeadHole = False
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..

<<<<<<< HEAD
=======
                    #holeの一段上(y-1)を見てBlockがある場合DeadHoleとして数える(塞がるのは評価マイナス)
                    if board[(y - 1) * self.board_data_width + x] != self.ShapeNone_index:
                        #DeadHole
                        hasDeadHole = True
                        deadholeCandidates[x] += 1

>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
<<<<<<< HEAD
                    nBlocksEachLine[y] += 1
=======
                    nBlocks[y] += 1
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9

                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                     
                        if holeConfirm[x] == 1:              #リーチのline(holeが一つだけの線)があるかどうか調べる
                            hasReach = True
                        else:
                            hasReach = False
                    
<<<<<<< HEAD
                    #Blockの一段下(y+1)を見て空白がある場合FloatingBlockとして数える(浮いているのは評価マイナス)
                    if y != height -1:
                        if board[(y + 1) * self.board_data_width + x] == self.ShapeNone_index:
                            #FloatingBlock
                            hasFloatingBlock = True
                            FloatingBlockCandidates[x] += 1
                            nFloatingBlocksEachLine[y] += 1

                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

                    if FloatingBlockCandidates[x] > 0:
                        FloatingBlockConfirm[x] += FloatingBlockCandidates[x]  # update number of holes in target column..
                        FloatingBlockCandidates[x] = 0                # reset
=======
                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

                    if deadholeCandidates[x] > 0:
                        deadholeConfirm[x] += deadholeCandidates[x]  # update number of holes in target column..
                        deadholeCandidates[x] = 0                # reset
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
                if fullLines == 4:
                    hasMaxfullLines = True
                elif fullLines == 3:
                    has3fullLines = True
                elif fullLines == 2:
                    has2fullLines = True
                else:
                    hasMaxfullLines = False
                    has3fullLines = False
                    has2fullLines = False
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass
            
            #リーチの本数を追加する
<<<<<<< HEAD
            if nBlocksEachLine[y] == width - 1 & nFloatingBlocksEachLine[y] == 0:
                # filled with block
                reachlines += 1

            if nBlocksEachLine[y] == width - 2 & nFloatingBlocksEachLine[y] == 0:
=======
            if nBlocks[y] == width - 1 :
                # filled with block
                reachlines += 1

            if nBlocks[y] == width - 2 :
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
                # filled with block
                w8lines += 1

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

<<<<<<< HEAD
        # nFloatingBlocks
        for x in FloatingBlockConfirm:
            nFloatingBlocks += abs(x)
=======
        # nDeadHoles
        for x in deadholeConfirm:
            nDeadHoles += abs(x)
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)


        # calc Evaluation Value
        score = 0
        score = score + reachlines * 10.0
<<<<<<< HEAD
        #score = score + w8lines * 5.0
        if hasMaxfullLines == True:
            score = score + fullLines *25.0
        elif has3fullLines == True:
            score = score + fullLines *5.0
        elif has2fullLines == True:
            score = score + fullLines *(-10.0)
        else :
            score = score +fullLines *(-10.0)
            
        #score = score + (fullLines/3) * 500.0 + (fullLines/4) +1000.0          # try to delete line 
        score = score - nHoles * 10.0                     # try not to make hole
        score = score - nFloatingBlocks * 20.0                     # try not to make hole
        #score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 1.0                # try to put block smoothly
        score = score - maxDy * 1.0                # maxDy
        score = score - maxHeight * 0.0              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        #print('score=', score ,'reach=', reachlines,'full=', fullLines, 'holes=', nHoles,'FloatingBlocks=', 
        #       nFloatingBlocks, 'IsolatedBlocks=', nIsolatedBlocks, 'maxHeiaght=',maxHeight, 'absDy=',absDy,'BlockMaxY=', BlockMaxY)
=======
        score = score + w8lines * 5.0
        if hasMaxfullLines == True:
            score = score + fullLines *100.0
        elif has3fullLines == True:
            score = score + fullLines *50.0
        elif has2fullLines == True:
            score = score + fullLines *0.0
        else :
            score = score +fullLines *0.0
            
        #score = score + (fullLines/3) * 500.0 + (fullLines/4) +1000.0          # try to delete line 
        score = score - nHoles * 10.0                     # try not to make hole
        score = score - nDeadHoles * 10.0                     # try not to make hole
        #score = score - nIsolatedBlocks * 1.0      # try not to make isolated block
        score = score - absDy * 1.0                # try to put block smoothly
        score = score - maxDy * 1.0                # maxDy
        score = score - maxHeight * 1.0              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        #print('score=', score ,'reach=', reachlines,'full=', fullLines, 'holes=', nHoles,'deadholes=', 
        #       nDeadHoles, 'IsolatedBlocks=', nIsolatedBlocks, 'maxHeiaght=',maxHeight, 'absDy=',absDy,'BlockMaxY=', BlockMaxY)
>>>>>>> ce8418c2b7de64eecf1d6902e0a713fabbb8fcb9
        #os.system('PAUSE')
        return score

BLOCK_CONTROLLER = Block_Controller()

