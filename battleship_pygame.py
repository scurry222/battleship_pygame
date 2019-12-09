#!C:\Users\SageLoaner\AppData\Local\Programs\Python\Python37-32\python.exe
import pygame as pg
import sys

def main():
  cellsz = 50
  player = [0,1]
  # once in beginning
  pg.init()
  screen = pg.display.set_mode((cellsz*20, cellsz*10), pg.HWSURFACE) # pg.FULLSCREEN | pg.HWSURFACE
  pg.display.set_caption("Best Battleship Ever")
  screen.convert()
  screen.set_colorkey((0, 0, 1))
  screen.fill((255, 127, 127))
  p = [0,1]
  p[0] = Player(cellsz=cellsz, ocean=(0,0,255))
  p[1] = Player(cellsz=cellsz, ocean=(0,128,255))
  p[0].setname("Player 1")
  p[1].setname("Player 2")
  p[0].board.draw_grid()
  p[1].board.draw_grid()

  targetsurf = pg.Surface((int(cellsz * 3 / 4), int(cellsz * 3 / 4))).convert()
  targetsurf.fill((0, 0, 0))
  targetsurf.set_colorkey((0, 0, 0))
  targetrect = targetsurf.get_rect()
  pg.draw.circle(targetsurf, (255, 0, 0), targetrect.center, int(targetrect.w / 2), 2)
  pg.draw.line(targetsurf, (255, 0, 0), targetrect.midleft, targetrect.midright, 2)
  pg.draw.line(targetsurf, (255, 0, 0), targetrect.midtop, targetrect.midbottom, 2)

  for player in p:
    player.add_ship(length = 5, name="carrier")
    player.add_ship(length = 4, name="battleship")
    player.add_ship(length = 3, name="cruiser")
    player.add_ship(length = 3, name="submarine")
    player.add_ship(length = 2, name="destroyer")
  
  punch_sound = load_sound('punch.wav')
  whiff_sound = load_sound('whiff.wav')

  placedir = 0 # 0 = Horizontal, 1 vertical
  p_up = 0
  ship_up = 0
  mpos = (0,0)
  gamephase = 0  # 0 = Placing ships, 1 = Shooting at ships

  running = True
  while running:

    place_valid = False
    # if len(p[0].ships) >= p[0].numships and len(p[1].ships) >= p[1].numships:
      # gamephase = 1
      # print("new gamephase = ", gamephase, "ship_up = ", ship_up, "p_up = ", p_up)
    nextphase = True
    if gamephase < 2:
      for ship in p[p_up].ships:
        if not ship.placed:
          nextphase = False
      if nextphase:
        ship_up = 0
        if p_up == 0:
          p_up = 1
        else:
          p_up = 0
        pg.time.wait(1000)
        gamephase += 1
    elif gamephase == 2:
      if p[0].sunk_all or p[1].sunk_all:
        gamephase = 3

    # Draw player boards containing existing ships, misses and hits
    if gamephase == 0:
      p[0].draw_ships(draw_all=True)
      p[1].board.draw_grid(p[1].ocean)

    elif gamephase == 1:
      p[1].draw_ships(draw_all=True)
      p[0].board.draw_grid(p[0].ocean)

    elif gamephase == 2:
      for player in p:
        player.draw_ships(draw_all=False)
        player.draw_hits()

    elif gamephase == 3:
      for player in p:
        player.draw_ships(draw_all=True)
        player.draw_hits()

    screen.blit(p[0].board.surf, (0, 0))
    screen.blit(p[1].board.surf, (cellsz*10, 0))

    placesquare = [int(mpos[0]/50), int(mpos[1]/50)] # Which square are we hovering over based on mouse


    # print("placesquare, p_up, placedir, ship_up, p[p_up].ships.length", placesquare, p_up, placedir, ship_up, p[p_up].ships[ship_up].length)
    # print(p[p_up].board.check_ship_fit((placesquare[0] - 10 * p_up, placesquare[1]), placedir, p[p_up].ships[ship_up].length))
    if gamephase < 2:
      if int(mpos[0] / (10 * cellsz)) == p_up and p[p_up].board.check_ship_fit([placesquare[0] - 10 * p_up, placesquare[1]], placedir, p[p_up].ships[ship_up].length):
        place_valid = True
    else:
      if int(mpos[0] / (10 * cellsz)) == p_up:
        place_valid = True

    if gamephase < 2:

      if placedir == 1:  # If vertical
        mousesurf = pg.Surface((int(cellsz/2), int(cellsz* p[p_up].ships[ship_up].length - cellsz / 2))).convert() # Rectangle to represent ship being placed (vertical)
      else:
        mousesurf = pg.Surface((int(cellsz * p[p_up].ships[ship_up].length - cellsz / 2), int(cellsz/2))).convert() # Rectangle to represent ship being placed (horizontal)

      mouserect = mousesurf.get_rect()  # Get rect data for ship being placed

      if place_valid:
        mousesurf.fill((200,200,200))  # Light gray
        pg.draw.rect(mousesurf, (50, 50, 50), mouserect, 1)  # Outline ship being placed
      else:
        mousesurf.fill((255,192,203))  # Light pink
        pg.draw.rect(mousesurf, (100, 50, 50), mouserect, 1)  # Outline ship being placed

      screen.blit(mousesurf, (placesquare[0]*cellsz+int(cellsz/4), placesquare[1]*cellsz+int(cellsz/4)))

      
    elif gamephase == 2:
      mousesurf = targetsurf
      mouserect = targetrect
      placesquare = [int(mpos[0]/50), int(mpos[1]/50)] # Which square are we hovering over based on mouse

      screen.blit(mousesurf, (placesquare[0]*cellsz+cellsz/8, placesquare[1]*cellsz+cellsz/8))
      

    pg.display.update()
    
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          running = False
        if event.key == pg.K_SPACE:
          if placedir == 0:
            placedir = 1
          else:
            placedir = 0
          # print("space dir=", placedir)
      if event.type == pg.MOUSEMOTION:
        mpos = pg.mouse.get_pos()
      if event.type == pg.MOUSEBUTTONDOWN:
        if place_valid:
          if p_up:
            placesquare[0] = placesquare[0]-10  # Correct x coordinate for player 2's map
          if gamephase < 2:
            p[p_up].place_ship(ship=p[p_up].ships[ship_up], coord=placesquare, direction=placedir, cellsz=cellsz)
            ship_up += 1
          elif gamephase == 2:
            success = p[p_up].incoming(coord=placesquare)
            if (success):
              punch_sound.play()
            else:
              whiff_sound.play()
            if p_up == 0:
              p_up = 1
            else:
              p_up = 0
          #pg.draw.rect(p1.surf, (255, 0, 0), (x, y, x + 50, y + 50))
          #print(x, y)

  sys.exit(2)

def load_sound(name):
  class NoneSound:
    def play(self): pass
  if not pg.mixer or not pg.mixer.get_init():
    return NoneSound()
  try:
    sound = pg.mixer.Sound(name)
  except pg.error:
    raise SystemExit(str(geterror()))
  return sound


class Player(object):
  def __init__(self, cellsz=50, ocean=(0,0,255)):
    self.name = "Player"
    self.board = Board()
    self.ocean = ocean
    self.cellsz = cellsz
    self.ships = []
    self.numships = 2
    self.placedships = 0
    self.sunk_all = False

    self.board = Board(cellsz=cellsz)

  def setname(self, name):
    self.name = name

  def add_ship(self, length=None, cellsz=50, name=None):
    # Add ship object to list of ships
    self.ships.append(Ship(length=length, cellsz=cellsz, name=name))

  def place_ship(self, ship, coord=[0,0], direction=None, cellsz=None):
    mycoord = coord.copy()
    self.board.new_ship(mycoord, direction, ship.length)
    ship.place(mycoord, direction)

    # self.board.surf.blit(ship.surf, (coord[0]*self.cellsz+int(self.cellsz/4), coord[1]*self.cellsz+int(self.cellsz/4)))

  def incoming(self, coord=[0,0]):
    got_hit = False
    mycoord = coord.copy()
    if self.board.cells[mycoord[0]][mycoord[1]] == 0:    # miss
      self.board.cells[mycoord[0]][mycoord[1]] = 3
    elif self.board.cells[mycoord[0]][mycoord[1]] == 1:  # hit!
      got_hit = True
      self.board.cells[mycoord[0]][mycoord[1]] = 2
      self.sunk_all = True
      for ship in self.ships:                                  # check all ships to see if theyve been sunk
        sunk = True
        for cell in ship.hull:
          if self.board.cells[cell[0]][cell[1]] == 1:
            sunk = False
        if sunk:
          ship.sink()
          # self.board.surf.blit(ship.surf, (coord[0]*self.cellsz+int(self.cellsz/4), coord[1]*self.cellsz+int(self.cellsz/4)))
        else:
          self.sunk_all = False
      return got_hit

  def draw_hits(self):
    for col in range(len(self.board.cells)):
      for row in range(len(self.board.cells[col])):
        if self.board.cells[col][row] == 2:
          self.board.draw_shot((col, row), (255, 0, 0))
        elif self.board.cells[col][row] == 3:
          self.board.draw_shot((col, row), (255, 255, 255))

  def draw_ships(self, draw_all=False):
    self.board.draw_grid(self.ocean)
    for ship in self.ships:
      if ship.sunk or draw_all and ship.placed:
        self.board.surf.blit(ship.surf, (ship.coord[0]*self.cellsz+int(self.cellsz/4), ship.coord[1]*self.cellsz+int(self.cellsz/4)))
        if ship.sunk:
          pg.draw.rect(self.board.surf, (255, 0, 0), (ship.coord[0]*self.cellsz+int(self.cellsz/4), ship.coord[1]*self.cellsz+int(self.cellsz/4), ship.rect.w, ship.rect.h), 3)




class Ship(object):
  def __init__(self, length=3, cellsz=50, name="unnamed"):
    self.length = length
    self.cellsz = cellsz
    self.placed = False
    self.name = name
    self.hull = []
    self.sunk = False
    self.surf = pg.Surface((0,0))

  def place(self, coord=[0,0], direction=None):
    self.direction = direction
    self.coord = coord.copy()
    self.placed = True

    if self.direction == 1:  # If vertical
      self.surf = pg.Surface((int(self.cellsz/2), int(self.cellsz* self.length - self.cellsz / 2))).convert() # Rectangle to represent ship being placed (vertical)
    else:
      self.surf = pg.Surface((int(self.cellsz * self.length - self.cellsz / 2), int(self.cellsz / 2))).convert() # Rectangle to represent ship being placed (horizontal)

    # print("coord = ", coord)
    self.hull.append(coord)
    i = 1
    while i < self.length:
      if direction:                               # vertical
        self.hull.append([coord[0], coord[1] + i])
      else:                                       # horizontal
        self.hull.append([coord[0] + i, coord[1]])
      i += 1
    # print(self.hull)

    self.rect = self.surf.get_rect()
    self.surf.fill((128,128,128)) # light grey
    pg.draw.rect(self.surf, (0,0,0), self.rect, 1)

  def sink(self):
    self.sunk = True

class Board(object):
  def __init__(self, cellsz=50):
    self.cells = [[0 for y in range(10)] for x in range(10)]
    self.cellSize = cellsz
    self.surf = pg.Surface((cellsz*len(self.cells), cellsz*len(self.cells))).convert()
    self.surf.set_colorkey((0,0,1))
    self.rect = self.surf.get_rect()

  def check_ship_fit(self, coord=[0,0], direction=None, length=0):
    mycoord = coord.copy()
    it_fits = True
    if (direction and mycoord[1] + length > 10) or (not direction and mycoord[0] + length > 10):
      it_fits = False
    else:
      for cell in range(length):
        # print(mycoord)
        if self.cells[mycoord[0]][mycoord[1]] != 0:
          it_fits = False
        if direction == 1:
          mycoord[1] = mycoord[1] + 1
        else:
          mycoord[0] = mycoord[0] + 1
    return it_fits

  def new_ship(self, coord=[0,0], direction=None, length=0):
    mycoord = coord.copy()
    for cell in range(length):
      self.cells[mycoord[0]][mycoord[1]] = 1
      # direction 1 = vertical, 0 = horizontal
      if direction == 1:
        mycoord[1] = mycoord[1] + 1
      else:
        mycoord[0] = mycoord[0] + 1

  def draw_grid(self, ocean=(0,0,255)):
    self.surf.fill(ocean)
    for row in range(len(self.cells)):
      for col in range(len(self.cells[row])):
        # print("rect = ", col * 50, row * 50, self.cellSize, self.cellSize)
        pg.draw.rect(self.surf, (0, 0, 0), (col * self.cellSize, row * self.cellSize, self.cellSize, self.cellSize), 1)

  def draw_shot(self, coord, color):
    # print("coord = ", coord[0])
    pg.draw.circle(self.surf, color, (coord[0] * self.cellSize + 25, coord[1] * self.cellSize + int(self.cellSize / 2)), int(self.cellSize / 5), 0)
    pg.draw.circle(self.surf, (50, 50, 50), (coord[0] * self.cellSize + 25, coord[1] * self.cellSize + int(self.cellSize / 2)), int(self.cellSize / 5), 1)


if (__name__ == '__main__'):
  main();