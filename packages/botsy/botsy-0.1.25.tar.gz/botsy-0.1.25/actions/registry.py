import json
import os

from tinydb import Query, TinyDB

name = "registry.db"
models_dir = os.environ.get("MODELS_DIR", "/Users/jfurr/test_models")
model_name = os.path.join(models_dir, name)
db_path = os.path.join(models_dir, model_name)


class ActionRegistry:
    """
    ActionRegistry is a singleton class that keeps track of isntalled actions
    """

    _instance = None

    def __new__(cls, db_path=db_path):
        if cls._instance is None:
            cls._instance = super(ActionRegistry, cls).__new__(cls)
            cls._instance.db = TinyDB(db_path)
            cls._instance.register_actions()
        return cls._instance

    def register_actions(self, actions_path=os.path.dirname(os.path.abspath(__file__))):
        for action in os.listdir(actions_path):
            action_path = os.path.join(actions_path, action)

            if os.path.isdir(action_path) and "manifest.json" in os.listdir(
                action_path
            ):
                manifest_path = os.path.join(action_path, "manifest.json")

                with open(manifest_path, "r") as f:
                    manifest = json.load(f)

                Action = Query()
                self.db.upsert(manifest, Action.name == manifest["name"])

    def clear_registry(self):
        self.db.truncate()

    def list_actions(self):
        return [action["name"] for action in self.db.all()]
