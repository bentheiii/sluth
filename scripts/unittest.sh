# run the unittests with branch coverage
set -e
coverage run --branch --include="sluth/*" -m pytest tests/ "$@"
coverage html
coverage report -m
coverage xml