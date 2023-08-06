import json
import os
import shutil
import unittest

from botsy.actions.registry import ActionRegistry


class TestActionRegistry(unittest.TestCase):
    def setUp(self):
        self.db_path = "test_db.json"

        # Create test actions
        self.test_dir = "test_actions"
        self.test_actions = ["test_actions1", "test_actions2", "test_actions3"]

        # remove old test actions
        self._remove_actions()
        os.makedirs(self.test_dir)
        os.environ["ACTION_DIR"] = self.test_dir

        for action in self.test_actions:
            action_dir = os.path.join(self.test_dir, action)
            os.makedirs(action_dir)
            with open(f"{action_dir}/manifest.json", "w") as f:
                json.dump({"name": action}, f)

        self.registry = ActionRegistry(self.db_path)
        self.registry.register_actions(actions_path=self.test_dir)

    def tearDown(self):
        self.registry.clear_registry()

        # Remove tinyDB test.db
        shutil.rmtree(self.db_path, ignore_errors=True)

        # Remove test_actions directory
        self._remove_actions()

        del self.registry

    def _remove_actions(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_singleton_instance(self):
        registry1 = ActionRegistry(self.db_path)
        registry2 = ActionRegistry(self.db_path)
        self.assertEqual(registry1, registry2)

    def test_clear_registry(self):
        self.registry.clear_registry()
        num_actions = len(self.registry.list_actions())
        self.assertEqual(num_actions, 0)

    def test_list_actions(self):
        result = self.registry.list_actions()
        self.assertEqual(set(result), set(self.test_actions))


if __name__ == "__main__":
    unittest.main()
