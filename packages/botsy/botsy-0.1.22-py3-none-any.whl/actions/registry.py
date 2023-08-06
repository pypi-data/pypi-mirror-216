import json
import os

from tinydb import Query, TinyDB

db_path = os.path.join(
    os.environ.get("PROJECT_ROOT"),
    os.environ.get("REGISTRY_DB"),
)


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

    def register_actions(self):
        actions_path = os.path.join(
            os.environ.get("PROJECT_ROOT"), os.environ.get("ACTION_DIR", "actions")
        )
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
