#!/bin/bash

# Specify the path to your pyproject.toml file
PYPROJECT_FILE="pyproject.toml"

# Get the current version from the pyproject.toml file
CURRENT_VERSION=$(awk -F '"' '/^version/ {print $2}' "$PYPROJECT_FILE")

# Increment the version
MAJOR=$(echo "$CURRENT_VERSION" | awk -F '.' '{print $1}')
MINOR=$(echo "$CURRENT_VERSION" | awk -F '.' '{print $2}')
PATCH=$(echo "$CURRENT_VERSION" | awk -F '.' '{print $3}')
NEW_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"

# Replace the version in the pyproject.toml file with the new version
sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" "$PYPROJECT_FILE"

echo "Version incremented from $CURRENT_VERSION to $NEW_VERSION"
