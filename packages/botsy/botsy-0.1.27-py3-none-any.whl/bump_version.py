#!/usr/bin/env python

import tomlkit

# Load the pyproject.toml file
with open("pyproject.toml", "r") as file:
    data = tomlkit.parse(file.read())

# Split the version string into major, minor, patch
major, minor, patch = map(int, data["tool"]["poetry"]["version"].split("."))

# Increase the minor version by 1
patch += 1

# Set the new version back to the toml data
data["tool"]["poetry"]["version"] = f"{major}.{minor}.{patch}"

# Write the updated toml data back to the file
with open("pyproject.toml", "w") as file:
    file.write(tomlkit.dumps(data))
