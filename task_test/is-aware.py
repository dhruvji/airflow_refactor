import unittest
import os
import ast

class TestAirflowTimezone(unittest.TestCase):
    
    def test_is_naive_function_exists(self):
        # Path to the file where the is_naive function should be defined
        file_path = '../airflow/utils/timezone.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the timezone.py file to check for the is_naive function
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_naive_function = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'is_naive':
                is_naive_function = node
                break

        self.assertIsNotNone(is_naive_function, "Function 'is_naive' not found in timezone.py")

    def test_is_aware_function_exists(self):
        # Path to the file where the is_aware function should be defined
        file_path = '../airflow/utils/timezone.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the timezone.py file to check for the is_aware function
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_aware_function = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'is_aware':
                is_aware_function = node
                break

        self.assertIsNotNone(is_aware_function, "Function 'is_aware' not found in timezone.py")

    def test_is_localized_not_exists(self):
        # Path to the file where we check that is_localized is not defined
        file_path = '../airflow/utils/timezone.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the timezone.py file to check for any references to is_localized
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_localized_found = False

        for node in ast.walk(tree):
            # Check for function definition
            if isinstance(node, ast.FunctionDef) and node.name == 'is_localized':
                is_localized_found = True
                break
            # Check for function usage
            if isinstance(node, ast.Name) and node.id == 'is_localized':
                is_localized_found = True
                break

        self.assertFalse(is_localized_found, "Function 'is_localized' was found in timezone.py, but it should not exist")

    def test_mark_tasks_does_not_use_is_localized(self):
        # Path to the mark_tasks.py file
        file_path = '../airflow/api/common/mark_tasks.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the mark_tasks.py file to ensure it does not use timezone.is_localized
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_localized_found = False
        is_aware_found = False

        for node in ast.walk(tree):
            # Check for timezone.is_localized usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_localized':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_localized_found = True
            # Check for timezone.is_aware usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_aware':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_aware_found = True

        self.assertFalse(is_localized_found, "'timezone.is_localized' was found in mark_tasks.py, but it should not be used")
        self.assertTrue(is_aware_found, "'timezone.is_aware' was not found in mark_tasks.py, but it should be used")

    def test_test_timezone_does_not_use_is_localized(self):
        # Path to the test_timezone.py file
        file_path = '../tests/utils/test_timezone.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the test_timezone.py file to ensure it does not use timezone.is_localized
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_localized_found = False
        is_aware_found = False

        for node in ast.walk(tree):
            # Check for timezone.is_localized usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_localized':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_localized_found = True
            # Check for timezone.is_aware usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_aware':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_aware_found = True

        self.assertFalse(is_localized_found, "'timezone.is_localized' was found in test_timezone.py, but it should not be used")
        self.assertTrue(is_aware_found, "'timezone.is_aware' was not found in test_timezone.py, but it should be used")

    def test_trigger_dag_does_not_use_is_localized(self):
        # Path to the trigger_dag.py file
        file_path = '../airflow/api/common/trigger_dag.py'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Parse the trigger_dag.py file to ensure it does not use timezone.is_localized
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        is_localized_found = False
        is_aware_found = False

        for node in ast.walk(tree):
            # Check for timezone.is_localized usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_localized':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_localized_found = True
            # Check for timezone.is_aware usage
            if isinstance(node, ast.Attribute) and node.attr == 'is_aware':
                if isinstance(node.value, ast.Name) and node.value.id == 'timezone':
                    is_aware_found = True

        self.assertFalse(is_localized_found, "'timezone.is_localized' was found in trigger_dag.py, but it should not be used")
        self.assertTrue(is_aware_found, "'timezone.is_aware' was not found in trigger_dag.py, but it should be used")

    def test_docs_does_not_use_is_localized(self):
        # Path to the timezone.rst file
        file_path = '../docs/apache-airflow/authoring-and-scheduling/timezone.rst'

        # Check if the file exists
        self.assertTrue(os.path.exists(file_path), f"{file_path} does not exist")

        # Read the file and check for the specific strings
        with open(file_path, 'r') as file:
            content = file.read()

        self.assertNotIn('timezone.is_localized()', content, "'timezone.is_localized()' was found in timezone.rst, but it should not be used")
        self.assertIn('timezone.is_aware()', content, "'timezone.is_aware()' was not found in timezone.rst, but it should be used")


if __name__ == '__main__':
    unittest.main()
