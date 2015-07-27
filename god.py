import operator as op
import functools as f
import subprocess as sp
import re

def __parseMove(str):
    cols = str.split()
    win = int(re.match('-?\d+', cols[3]).group(0))
    cnt = int(re.search('\((\d+)\)', cols[3]).group(1))
    return cols[2], win, cnt

def getMovesWithScore(board, turn):
    turnStr = '+' if turn == 1 else '-'
    rows = f.reduce(op.concat, board) + ['000000', turnStr]
    rows = list(map(lambda r: r + '\n', rows))
    arg = f.reduce(op.concat, rows)

    cmd = "god/checkStateIO"
    p = sp.Popen(cmd, stdin=sp.PIPE, stdout=sp.PIPE)
    out, _ = p.communicate(bytes(arg, 'ascii'))

    lines = out.decode('utf-8').split('\n')
    # 候補手リストまで読む
    idx = 0
    while not lines[idx].count(':'):
        idx += 1
    # 候補手リスト作成
    moves = []
    while lines[idx].count(':') and not lines[idx].count('Move'):
        moves.append(__parseMove(lines[idx]))
        idx += 1

    best = __parseMove(lines[idx])

    return moves, best

stoneName = {
        "HI": "ひよこ",
        "KI": "きりん",
        "LI": "ライオン",
        "ZO": "ぞう",
        "NI": "にわとり"
        }

def __movesHum(desc):
    return '{0}{1}({2})'.format(desc[3:5], stoneName[desc[5:]], desc[1:3])

def __message(turn, win, cnt):
    if win == 0:
        return "引き分けだよ"
    return "あと{0}手できみの{1}だよ٩(๑❛ᴗ❛๑)۶".format(cnt, "勝ち" if turn != win else "負け")

def godMessage(board, turn):
    _, best = getMovesWithScore(board, turn)
    return __movesHum(best[0]), __message(turn, best[1], best[2])

#board = [['-LI' ' . ' '-ZO'],
#        ['-KI' '-HI' '+KI'],
#        ['+HI' '+ZO' ' . '],
#        [' . ' '+LI' ' . ']]
#board = [['-KI' '-LI' '-ZO'],
#        [' . ' '-HI' ' . '],
#        [' . ' '+HI' ' . '],
#        ['+ZO' '+LI' '+KI']]
#moves = getMovesWithScore(board, '-')
#print(moves)
#print(godMessage(board, 1))
