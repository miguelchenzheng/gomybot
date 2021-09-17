# bot.py

# Imports
import os
import random
import discord
import numpy as np

from discord.ext import commands
from dotenv import load_dotenv

# Carga el .env con datos del Token del bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# Elige el prefijo
bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")


@bot.command()
async def print(ctx, arg):
    await ctx.channel.send(arg)


@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

import numpy as np

# Board Size
Board_Size = 15
Frame_Gap = 35
width = 700
height = 700


def Location_Validation(X,Y):
    if X == None or Y == None:
        return False

    elif board[Y - 1][X - 1] == 0:
        return True


def Score_Board():
    print(f"{Winner} ha ganado la partida")


def winCheck(Piece_Number, Piece_Colour, board):
    if rowCheck(Piece_Number, board) or rowCheck(Piece_Number, transpose(board)) or rowCheck(Piece_Number,
                                                                                             transposeDiagonalInc(
                                                                                                 board)) or rowCheck(
        Piece_Number, transposeDiagonalDec(board)):
        Winner = Piece_Colour
        return Winner


def rowCheck(Piece_Number, board):
    for i in range(len(board)):
        if board[i].count(Piece_Number) >= 5:

            for z in range(len(board) - 3):
                Connection = 0

                for c in range(5):
                    if board[i][z + c] == Piece_Number:
                        Connection += 1

                    else:
                        break

                    if Connection == 5:
                        return True


def getDiagonalDec(loa, digNum):
    lst = []
    if digNum <= len(loa) - 1:
        index = len(loa) - 1
        for i in range(digNum, -1, -1):
            lst.append(loa[i][index])
            index -= 1
        return lst
    else:
        index = (len(loa) * 2 - 2) - digNum
        for i in range(len(loa) - 1, digNum - len(loa), -1):
            lst.append(loa[i][index])
            index -= 1
        return lst


def transposeDiagonalDec(loa):
    lst = []
    for i in range(len(loa) * 2 - 1):
        lst.append(getDiagonalDec(loa, i))
    return lst


def getDiagonalInc(loa, digNum):
    lst = []
    if digNum <= len(loa) - 1:
        index = 0
        for i in range(digNum, -1, -1):
            lst.append(loa[i][index])
            index += 1
        return lst
    else:
        index = digNum - len(loa) + 1
        for i in range(len(loa) - 1, digNum - len(loa), -1):
            lst.append(loa[i][index])
            index += 1
        return lst


def transposeDiagonalInc(loa):
    lst = []
    for i in range(len(loa) * 2 - 1):
        lst.append(getDiagonalInc(loa, i))
    return lst


def transpose(loa):
    lst = []
    for i in range(len(loa)):
        lst.append(getCol(loa, i))
    return lst


def getCol(loa, colNum):
    lst = []
    for i in range(len(loa)):
        lst.append(loa[i][colNum])
    return lst


def Exit():
    global Winner
    Winner = "Exit"

@bot.command()
async def coordenada(ctx):
    if Turn == "white":
        await ctx.send("Turno Blanco:")

    elif Turn == "black":
        await ctx.send("Turno Negro:")
    # y = int(input('Coordenadas x:'))
    # x = int(input('Coordenadas y:'))
    y,x = await coord()

    await setTablero(x, y)
    await Tablero(ctx)
    return x, y

@bot.command()
async def setTablero(ctx,coorx, coory):
    if Turn == 'white':
        matriz[coorx, coory] = 1
    elif Turn == 'black':
        matriz[coorx, coory] = 2

@bot.command()
async def tablero(ctx):
    linea =""
    for fila in matriz:
        for elemento in fila:
            if elemento == 0:
                linea += ("     ·")
            elif elemento == 1:
                linea += ("     o")
            elif elemento == 2:
                linea += ("     x")
        await ctx.send(linea)
        linea = ""


@bot.command("turn")
async def coord(ctx, posx: int, posy: int):
    cx = posx
    cy = posy
    return cx, cy



# Turn
Turn_Num = 1
Turn = "white"
Winner = None

# Cord List
Black_Cord_PickedX = []
Black_Cord_PickedY = []
White_Cord_PickedX = []
White_Cord_PickedY = []

# 2D Board List
board = []
matriz = np.zeros((15, 15), dtype=int)

# 2D list for Gameboard
for i in range(Board_Size + 1):
    board.append([0] * (Board_Size + 1))

Unfilled = 0
Black_Piece = 1
White_Piece = 2

# Game Code
@bot.command(name='game')
async def gomoku(ctx, p1: discord.Member, p2: discord.Member):
    global Winner
    await tablero(ctx)
    while Winner == None:
        X, Y = await coordenada(ctx)
        Picked = Location_Validation(X,Y)

        if Picked:
            if Turn_Num % 2 == 1:
                White_Cord_PickedX.append(X)
                White_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 2
                Turn = "black"


            elif Turn_Num % 2 == 0:
                Black_Cord_PickedX.append(X)
                Black_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 1
                Turn = "white"

            Turn_Num = Turn_Num + 1

            if Turn == "white":
                Colour_Check = Black_Piece
                Win_Check = "Black"

            elif Turn == "black":
                Colour_Check = White_Piece
                Win_Check = "White"

            Winner = winCheck(Colour_Check, Win_Check, board)

    if Winner != "Exit":
        Score_Board()


bot.run(TOKEN)
