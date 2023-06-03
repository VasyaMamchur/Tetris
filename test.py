import unittest
from unittest.mock import patch
from main import App, Tetris,  MOVE_DIRECTIONS
from figurines import Tetromino, Block
from settings import *

class TetrisTestCase(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.tetris = Tetris(self.app)
        self.tetromino = Tetromino(self.tetris)
        self.tetromino.blocks = [
            Block(self.tetromino, vec(5, 18)),
            Block(self.tetromino, vec(6, 18)),
            Block(self.tetromino, vec(5, 17)),
            Block(self.tetromino, vec(6, 17))
        ]
        self.tetris.tetromino = self.tetromino

    def tearDown(self):
        self.app = None

    def test_tetromino_move_left(self):
        initial_positions = [block.pos for block in self.tetris.tetromino.blocks]
        self.tetris.control(pressed_key='left')
        new_positions = [block.pos for block in self.tetris.tetromino.blocks]
        expected_positions = [pos - MOVE_DIRECTIONS['left'] for pos in initial_positions]
        self.assertEqual(new_positions, expected_positions)

    def test_tetromino_move_right(self):
        initial_positions = [block.pos for block in self.tetris.tetromino.blocks]
        self.tetris.control(pressed_key='right')
        new_positions = [block.pos for block in self.tetris.tetromino.blocks]
        expected_positions = [pos + MOVE_DIRECTIONS['right'] for pos in initial_positions]
        self.assertEqual(new_positions, expected_positions)

    def test_tetromino_move_down(self):
        initial_positions = [block.pos for block in self.tetris.tetromino.blocks]
        self.tetris.control(pressed_key='down')
        new_positions = [block.pos for block in self.tetris.tetromino.blocks]
        expected_positions = [pos + MOVE_DIRECTIONS['down'] for pos in initial_positions]
        self.assertEqual(new_positions, expected_positions)
    def test_tetromino_rotate(self):
        initial_positions = [block.pos for block in self.tetris.tetromino.blocks]
        self.tetris.control(pressed_key='up')
        new_positions = [block.pos for block in self.tetris.tetromino.blocks]
        expected_positions = initial_positions
        self.assertEqual(new_positions, expected_positions)

    @patch.object(Tetromino, 'is_collide')
    def test_check_tetromino_landing(self, mock_is_collide):
        mock_is_collide.return_value = True

        self.tetris.check_tetromino_landing()

        self.assertEqual(self.tetromino.blocks[0].pos, vec(9, 18))
        self.assertEqual(self.tetromino.blocks[1].pos, vec(10, 18))
        self.assertEqual(self.tetromino.blocks[2].pos, vec(9, 17))
        self.assertEqual(self.tetromino.blocks[3].pos, vec(10, 17))

        self.tetris.tetromino = self.tetris.next_tetromino

        self.assertIsInstance(self.tetris.next_tetromino, Tetromino)

        self.assertEqual(self.tetris.tetromino, self.tetris.next_tetromino)

    def test_tetris_initialization(self):
        self.assertIsInstance(self.app, App)
        self.assertEqual(self.app.music_playing, False)
        self.assertEqual(len(self.app.images), 8)


if __name__ == '__main__':
    unittest.main()