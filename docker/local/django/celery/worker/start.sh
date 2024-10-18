#!/bin/bash

# Restarts celery worker when code changes using watcher
set -o errexit
set -o nounset

# only monitor .py files "--filter python"
# celery.__main__.main is the entrypoint for celery (equivalent of running celery command in terminal)
# -A config.celery_app worker -l INFO are the arguments to pass to celery
exec watchfiles --filter python celery.__main__.main --args '-A config.celery_app worker -l INFO'