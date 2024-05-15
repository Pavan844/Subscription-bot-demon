from logging import (
    INFO,
    StreamHandler,
    basicConfig,
)
from logging import (
    error as log_error,
)
from logging import (
    info as log_info,
)
from logging.handlers import RotatingFileHandler
from os import getenv
from os import path as opath
from subprocess import run as srun

from dotenv import load_dotenv

basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=50000000, backupCount=10),
        StreamHandler(),
    ],
)
load_dotenv("config.env", override=True)

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

if UPSTREAM_REPO:
    if opath.exists(".git"):
        srun(["rm", "-rf", ".git"])

    update = srun(
        [
            f"git init -q \
                     && git config --global user.email drxxstrange@gmail.com \
                     && git config --global user.name SilentDemonSD \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"
        ],
        shell=True,
    )

    if update.returncode == 0:
        log_info("Successfully updated with latest commit from UPSTREAM_REPO")
    else:
        log_error(
            "Something went wrong while updating, check UPSTREAM_REPO if valid or not!"
        )
