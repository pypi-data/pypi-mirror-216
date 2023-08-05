# Don't forget to increment version when updating package

publish:
	python3 -m pip install --upgrade pip; \
	python3 -m pip install --upgrade build twine; \
	echo "Deleting dist/ folder in preparation to build new package"; \
	sudo rm -R dist; python3 -m build; python3 -m twine upload dist/*;

publish-autoinc:
	echo "Auto-incrementing version in pyproject.toml file"; \
	chmod +x inc_version.sh; \
	./inc_version.sh; \
	make publish;
