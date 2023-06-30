from typing import List
from unittest import TestCase
from unittest.mock import patch, MagicMock, call
import main
from main import *
from tests.mocks.mock_process import MockProcess

import psutil

@patch("builtins.print")
class TestMain(TestCase):
    def create_mock_processes(self, n_processes: int = 1) -> List[MockProcess]:
        processes = []

        for i in range(n_processes):
            process = MockProcess(i, f"proc_{i}")
            processes.append(process)

        return processes

    @patch.object(psutil, "process_iter", return_value=[])
    def test_killing_process_returns_false_when_no_running_processes_are_found(self, *_):
        # Act
        result = kill_process_by_name("process_name")

        # Assert
        self.assertFalse(result)

    @patch.object(psutil, "process_iter")
    def test_killing_process_returns_false_when_process_is_not_found(self, mock_process_iter, *_):
        # Arrange
        running_processes = self.create_mock_processes(3)
        mock_process_iter.return_value = running_processes
        
        # Act
        result = kill_process_by_name("fake_process")

        # Assert
        self.assertFalse(result)
        self.assertEqual(3, len([p for p in running_processes if p.running is True]))

    @patch.object(psutil, "process_iter")
    def test_killing_process_returns_true_when_process_has_been_killed(self, mock_process_iter, *_):
        # Arrange
        running_processes = self.create_mock_processes(3)
        mock_process_iter.return_value = running_processes
        
        # Act
        result = kill_process_by_name("proc_1")

        # Assert
        self.assertTrue(result)
        self.assertEqual(2, len([p for p in running_processes if p.running is True]))

    @patch.object(psutil, "process_iter")
    def test_getting_process_list_does_not_print_any_process(self, _, mock_print: MagicMock):
        # Act
        list_processes()

        # Assert
        mock_print.assert_not_called()

    @patch.object(psutil, "process_iter")
    def test_getting_process_list_does_prints_three_processes(self, mock_process_iter, mock_print: MagicMock):
        # Arrange
        running_processes = self.create_mock_processes(3)
        mock_process_iter.return_value = running_processes
        expected_prints=[call(f"\033[0m{proc.info['pid']}\t\033[32m{proc.info['pid']}\t{proc.info['name']}\033[0m") for proc in running_processes]
        
        # Act
        list_processes()

        # Assert
        mock_print.assert_has_calls(expected_prints)

    @patch.object(sys, "exit")
    @patch.object(main, "list_processes")
    def test_executing_script_calls_list_process_function_once(self, mock_list_processes: MagicMock, mock_exit: MagicMock, mock_print: MagicMock, *_):
        # Act
        py_killer(["-l"])

        # Assert
        mock_list_processes.assert_called_once_with()
        mock_exit.assert_not_called()
        mock_print.assert_called_once()

    @patch.object(sys, "exit")
    @patch.object(main, "kill_process_by_name", return_value=True)
    def test_executing_script_returns_none_when_kill_process_by_name_function_works(self, mock_kill_process_by_name: MagicMock, mock_exit: MagicMock, mock_print: MagicMock, *_):
        # Act
        py_killer(["-n", "process"])

        # Assert
        mock_kill_process_by_name.assert_called_once_with("process")
        mock_exit.assert_not_called()
        mock_print.assert_called_once()

    @patch.object(sys, "exit")
    @patch.object(main, "kill_process_by_name", return_value=False)
    def test_executing_script_returns_one_when_kill_process_by_name_function_fails(self, mock_kill_process_by_name: MagicMock, mock_exit: MagicMock, mock_print: MagicMock, *_):
        # Act
        py_killer(["-n", "process"])

        # Assert
        mock_kill_process_by_name.assert_called_once_with("process")
        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_once()

    @patch.object(sys, "exit")
    @patch.object(main, "kill_process_by_name", return_value=False)
    def test_executing_script_returns_two_when_process_to_kill_is_not_provided(self, _, mock_exit: MagicMock, mock_print: MagicMock, *__):
        # Act
        py_killer(["-n", ""])

        # Assert
        mock_exit.assert_called_once_with(2)
        self.assertEqual(2, mock_print.call_count)

    @patch.object(sys, "exit")
    @patch.object(main, "kill_process_by_name", return_value=False)
    def test_executing_script_returns_two_when_arguments_are_not_valid(self, _, mock_exit: MagicMock, mock_print: MagicMock, *__):
        # Act
        py_killer(["invalid_argument"])

        # Assert
        mock_exit.assert_called_once_with(2)
        self.assertEqual(2, mock_print.call_count)

    @patch.object(sys, "exit")
    @patch.object(main, "kill_process_by_name", return_value=False)
    def test_executing_script_returns_two_when_arguments_are_not_valid(self, _, mock_exit: MagicMock,  mock_print: MagicMock, *__):
        mock_exit.side_effect = lambda x: exit(x)

        # Act
        self.assertRaises(SystemExit, py_killer, ["-f"])
        
        # Assert
        mock_exit.assert_called_once_with(2)
        self.assertEqual(2, mock_print.call_count)