import pygame as pg
import remgine

WindowWidth = 1920
WindowHeight = 1080
ScreenWidth = 768
ScreenHeight = 432
PlayerStartX = 64
PlayerStartY = 64
PlayerWidth = 32
PlayerHeight = 32
Speed = 2

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
        remgine.Frame(200, (96, 48, 16, 16)),
        remgine.Frame(200, (112, 48, 16, 16)),
        remgine.Frame(200, (96, 64, 16, 16))
    ])