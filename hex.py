from typing import List, Set, Tuple, Dict, Optional
from enum import IntEnum

class Token(IntEnum):
    A = 1
    B = 2

class HexState():
    def __init__(self, size):
        self.size: int = size
        self.board: List[List[Optional[Token]]] = [[None for _ in range(size)] for _ in range(size)]
    
    def validateKey(self, key: Tuple[int, int]) -> bool:
        assert 0 <= key[0] < self.size, "key[0] out of bounds"
        assert 0 <= key[1] < self.size, "key[1] out of bounds"

    def __setitem__(self, key: Tuple[int, int], value: Token) -> None:
        self.validateKey(key)
        assert self[key] is None
        self.board[key[0]][key[1]] = value
    
    def __getitem__(self, key: Tuple[int, int]) -> Optional[Token]:
        self.validateKey(key)
        return self.board[key[0]][key[1]]
    
    def __delitem__(self, key: Tuple[int, int]) -> None:
        self.validateKey(key)
        self.board[key[0]][key[1]] = None
    
    def __str__(self) -> str:
        ret: str = ""
        sentinel: str = "  "
        for idx, row in enumerate(self.board):
            ret += sentinel * idx
            ret += sentinel.join([t.name if t is not None else "*" for t in row])
            ret += "\n"
        return ret

    def __eq__(self, o: object) -> bool:
        if isinstance(o, HexState):
            if o.size == self.size:
                for i in range(self.size):
                    for j in range(self.size):
                        if self[(i,j)] != o[(i,j)]:
                            return False
                return True
        return False
    
    def __lt__(self, o: object) -> bool:
        if isinstance(o, HexState):
            if o.size == self.size:
                for i in range(self.size):
                    for j in range(self.size):
                        if self[(i,j)] != o[(i,j)] and self[(i,j)] is not None:
                            return False
                return True
        return False
    
    


state0 = HexState(7)
state1 = HexState(7)
state0[(2,3)] = Token.A
print(state1 < state0)