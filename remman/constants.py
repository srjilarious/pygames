import pygame as pg
import remgine
import enum

WindowWidth = 1280
WindowHeight = 720
ScreenWidth = 384
ScreenHeight = 216
PlayerStartX = 64
PlayerStartY = 64
PlayerWidth = 32
PlayerHeight = 32
Speed = 0.1

class Direction(enum.Enum):
    Stopped = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4

# BluePiece = pg.image.load("blue_piece.png")
SpriteSheet = pg.image.load("assets/pac-tiles.png")

RedGhostRightFrames = remgine.Frames(SpriteSheet, 
    [ 
        remgine.Frame(400, (0, 16, 16, 16)),
        remgine.Frame(400, (16, 16, 16, 16))
    ])

RedGhostUpFrames = remgine.Frames(SpriteSheet, 
    [ 
        remgine.Frame(400, (32, 16, 16, 16)),
        remgine.Frame(400, (48, 16, 16, 16))
    ])

RedGhostDownFrames = remgine.Frames(SpriteSheet, 
    [ 
        remgine.Frame(400, (64, 16, 16, 16)),
        remgine.Frame(400, (80, 16, 16, 16))
    ])

MsPacManFrames = remgine.Frames(SpriteSheet,
    [
        remgine.Frame(200, (96, 48, 16, 16), (4,3),(2,3)),
        remgine.Frame(200, (112, 48, 16, 16), (4,3), (2,3)),
        remgine.Frame(200, (96, 64, 16, 16), (4,3), (2,3))
    ])

DotFrames = remgine.Frames(SpriteSheet,
    [
        remgine.Frame(200, (0, 8, 8, 8))
    ])

PowerDotFrames = remgine.Frames(SpriteSheet,
    [
        remgine.Frame(200, (8, 8, 8, 8))
    ])