import unittest
from unittest.mock import patch, MagicMock
import mysql.connector

# Import functions to be tested
from calculator_app import fetch_history, insert_history, delete_all_history, update_expression, update_history_expression, calculate_expression, button_action

class TestCalculatorApp(unittest.TestCase):

    @patch('calculator_app.mysql.connector.connect')
    def setUp(self, mock_connect):
        # Mock database connection and cursor
        self.mock_db = mock_connect.return_value
        self.mock_cursor = self.mock_db.cursor.return_value

        # Set up initial mock database state
        self.mock_cursor.fetchall.return_value = [
            ('1+1', '2'),
            ('2*2', '4')
        ]

    def test_fetch_history(self):
        history = fetch_history()
        self.mock_cursor.execute.assert_called_once_with("SELECT expression, result FROM history ORDER BY id DESC")
        self.assertEqual(history, [('1+1', '2'), ('2*2', '4')])

    def test_insert_history(self):
        insert_history('3+3', '6')
        self.mock_cursor.execute.assert_called_once_with("INSERT INTO history (expression, result) VALUES (%s, %s)", ('3+3', '6'))
        self.mock_db.commit.assert_called_once()

    def test_delete_all_history(self):
        global histories
        histories = [('1+1', '2'), ('2*2', '4')]
        delete_all_history()
        self.mock_cursor.execute.assert_called_once_with("DELETE FROM history")
        self.mock_db.commit.assert_called_once()
        self.assertEqual(histories, [])

    @patch('calculator_app.expression_label')
    def test_update_expression(self, mock_label):
        update_expression('5+5')
        mock_label.configure.assert_called_once_with(text='5+5')

    @patch('calculator_app.history_expression_label')
    def test_update_history_expression(self, mock_label):
        update_history_expression('5+5')
        mock_label.configure.assert_called_once_with(text='5+5')

    @patch('calculator_app.insert_history')
    @patch('calculator_app.expression_label')
    def test_calculate_expression(self, mock_label, mock_insert_history):
        global histories
        histories = []
        calculate_expression('5+5')
        mock_label.configure.assert_called_once_with(text='10')
        self.assertEqual(histories, [('5+5', '10')])
        mock_insert_history.assert_called_once_with('5+5', '10')

    @patch('calculator_app.update_expression')
    @patch('calculator_app.delete_all_history')
    def test_button_action(self, mock_delete_all_history, mock_update_expression):
        global expression
        expression = '5+5'

        # Test 'AC' button action
        button_action('AC')
        mock_update_expression.assert_called_with('')
        self.assertEqual(expression, '')

        # Test '<' button action
        expression = '5+5'
        button_action('<')
        mock_update_expression.assert_called_with('5+')
        self.assertEqual(expression, '5+')

        # Test '=' button action
        with patch('calculator_app.calculate_expression') as mock_calculate_expression:
            button_action('=')
            mock_calculate_expression.assert_called_once_with('5+5')

        # Test number button action
        button_action('1')
        mock_update_expression.assert_called_with('5+51')
        self.assertEqual(expression, '5+51')

if __name__ == '__main__':
    unittest.main()
