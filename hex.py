from typing import List, Set, Tuple, Optional
from enum import IntEnum


class Token(IntEnum):
    A = -1
    B = 1


class HexState:
    def __init__(self, size):
        self.size: int = size
        self.board: List[List[Optional[Token]]] = [[None for _ in range(size)] for _ in range(size)]

    def validate_key(self, key: Tuple[int, int]) -> None:
        assert 0 <= key[0] < self.size, "key[0] out of bounds"
        assert 0 <= key[1] < self.size, "key[1] out of bounds"

    def __setitem__(self, key: Tuple[int, int], value: Token) -> None:
        self.validate_key(key)
        self.board[key[0]][key[1]] = value

    def __getitem__(self, key: Tuple[int, int]) -> Optional[Token]:
        self.validate_key(key)
        return self.board[key[0]][key[1]]

    def __delitem__(self, key: Tuple[int, int]) -> None:
        self.validate_key(key)
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
                        if self[(i, j)] != o[(i, j)]:
                            return False
                return True
        return False

    def __lt__(self, o: object) -> bool:
        if isinstance(o, HexState):
            if o.size == self.size:
                for i in range(self.size):
                    for j in range(self.size):
                        if self[(i, j)] != o[(i, j)] and self[(i, j)] is not None:
                            return False
                return True
        return False


class HexGame:
    def __init__(self, size: int) -> None:
        assert 5 <= size <= 19, "board size must be between 5 and 19"
        self.size: int = size
        self.state: HexState = HexState(self.size)
        self.moves: List[Tuple[int, int]] = list()
        self.swapped: bool = False
        self.curToken: Token = Token.A
        self.valid: Set[Tuple[int, int]] = set([(i, j) for i in range(self.size) for j in range(self.size)])

    def flip_token(self) -> None:
        self.curToken = Token.A if self.curToken == Token.B else Token.B

    def place(self, move: Tuple[int, int]) -> None:
        assert move in self.valid, "invalid move"
        self.state[move] = self.curToken
        self.moves.append(move)
        self.valid.remove(move)
        self.flip_token()

    def undo(self) -> None:
        if len(self.moves) == 0:
            return
        elif len(self.moves) == 1 and self.swapped is True:
            self.state[self.moves[0]] = self.curToken
            self.swapped = False
        else:
            move = self.moves.pop()
            del self.state[move]
            self.valid.add(move)
        self.flip_token()

    def swap(self) -> None:
        assert len(self.moves) == 1 and self.swapped is False, "can only swap after first move"
        self.swapped = True
        self.state[self.moves[0]] = self.curToken
        self.flip_token()

    def __str__(self) -> str:
        return str(self.state)


if __name__ == "__main__":
    game = HexGame(7)
    print(str(game))
    game.place((2, 3))
    print(str(game))
    game.swap()
    print(str(game))
    game.place((3, 2))
    print(str(game))
    game.undo()
    print(str(game))
    game.undo()
    print(str(game))
    game.undo()
    print(str(game))
    game.undo()
    print(str(game))
