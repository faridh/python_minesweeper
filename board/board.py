from collections import defaultdict
from random import randrange

class Board:

  size: int
  number_of_mines: int
  cells: list[list[str]]
  hints: list[list[int]]
  adj_map: dict[tuple[int, int], set[tuple[int, int]]]
  mine_positions: set[tuple[int, int]]
  __game_ended: bool

  def __init__(self, size, number_of_mines):
    self.size = size
    self.number_of_mines = number_of_mines
    self.cells = []
    self.hints = []
    self.adj_map = defaultdict(set)
    self.mine_positions = set()
    self.__game_ended = False

    self.__init_empty_board()
    self.__place_mines()
    self.__fill_hints()
    self.__fill_adj_map()

  def __init_empty_board(self):
    self.cells = [[' ' for _ in range(self.size)] for _ in range(self.size)]
    self.hints = [[0 for _ in range(self.size)] for _ in range(self.size)]

  def __place_mines(self):
    placed_mines: int = 0
    while placed_mines < self.number_of_mines:
      random_row = randrange(0, self.size)
      random_col = randrange(0, self.size)
      if (random_row, random_col) not in self.mine_positions:
        self.mine_positions.add((random_row, random_col))
        placed_mines += 1

  def __fill_hints(self):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    for row, x in enumerate(self.cells):
      for col, y in enumerate(self.cells[row]):
        adjacent_mines: int = 0
        for d in directions:
          delta_row , delta_col = d[0], d[1]
          new_row = row + delta_row
          new_col = col + delta_col
          if 0 <= new_row < self.size and 0 <= new_col < self.size:
            if (new_row, new_col) in self.mine_positions:
              adjacent_mines += 1
        self.hints[row][col] = adjacent_mines

  def __fill_adj_map(self):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1), (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    for row, x in enumerate(self.hints):
      for col, y in enumerate(self.hints[row]):
        if self.hints[row][col] == 0 and (row, col) not in self.mine_positions:
          for d in directions:
            delta_row , delta_col = d[0], d[1]
            new_row = row + delta_row
            new_col = col + delta_col
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
              if self.hints[new_row][new_col] == 0:
                self.adj_map[(row, col)].add((new_row, new_col))

  def click(self, row: int, col: int) -> bool:
    if row < 0 or col < 0 or row > self.size or col > self.size:
      return True
    if self.game_ended:
      return False
    if self.cells[row][col] != ' ':
      return True

    if (row, col) in self.mine_positions:
      self.__end_game(True)
      return False
    else:
      if self.hints[row][col] == 0:
        origin = (row, col)
        stack = [origin]
        seen = set()
        while stack:
          node = stack.pop()
          if node in seen:
            continue
          seen.add(node)
          self.cells[node[0]][node[1]] = '0'
          for neighbor in self.adj_map[node]:
            stack.append(neighbor)
        if self.has_won():
          self.__end_game(False)
        return True
      else:
        self.cells[row][col] = f'{self.hints[row][col]}'
        if self.has_won():
          self.__end_game(False)
        return True

  def has_won(self) -> bool:
    empty_cells = 0
    for x in self.cells:
      for y in x:
        if y == ' ':
          empty_cells += 1
    if empty_cells == self.number_of_mines:
      return True
    return False

  def __end_game(self, lost: bool):
    self.__reveal_mines()
    self.__game_ended = True
    if lost:
      print(f'You lost the game')
    else:
      print(f'You won the game')

  def __reveal_mines(self):
    for (row, col) in self.mine_positions:
      self.cells[row][col] = 'X'

  @property
  def game_ended(self):
      return self.__game_ended

  def print_visual_board(self):
    for x in self.cells:
      print(f'{x}\n')

  def __repr__(self) -> str:
    printable_board: str = 'Board:\n'
    for x in self.cells:
      printable_board += f'{x}\n'
    printable_board += '\nHints:\n'
    for x in self.hints:
      printable_board += f'{x}\n'
    printable_board += '\nMines:\n'
    printable_board += f'{self.mine_positions}\n'
    return printable_board
