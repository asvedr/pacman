import logic.path_finder as Pf
import logic.logic as Lg
import logic.field as Field
import logic.pers as Pers
import unittest
import os
import types
import mock

class TestFinder(unittest.TestCase):

    def test_simple_search(self):

        field = Field.Field(os.path.join(os.path.dirname(__file__), 'search_test.txt'))
        namespace = types.SimpleNamespace()
        logic = Lg._LogicProcess(field, namespace)
        ghost = logic.ghosts[0]
        pacman = logic.pacman
        self.assertEqual(ghost.x, 1)
        self.assertEqual(ghost.y, 1)
        self.assertEqual(pacman.x, 4)
        self.assertEqual(pacman.y, 3)

        path = Pf.find_path(logic.field.data, [], pacman.point(), ghost.point())
        self.assertEqual(path, [(1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3)])

        self.assertTrue(ghost.is_on_cell_center())
        self.assertTrue(ghost.can_turn(logic.field.data))

        move_called = False

        def move_method(_self, _logic, nx, ny):
            if _self.color is None:
                # Case of pacman
                return
            nonlocal move_called
            move_called = True
            self.assertEqual((nx, ny), (2, 1))

        with mock.patch.object(Pers.Pers, 'regular_move', new=move_method):
            with mock.patch.object(Pers, 'RED_SPEED', new=1.0):
                logic.tick()
        self.assertTrue(move_called)
