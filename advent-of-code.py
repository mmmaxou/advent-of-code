# -*- coding: utf-8 -*-

# @author Maximilien Pluchard

import sys
import os
import platform
import json
import logging

software = u"design"
project = "creature-cases"
os.environ["TT_PROD_NAME"] = project
os.environ["TT_ENVIRONMENT_PATH"] = "E:/sandbox/tech_local/python_env.yml"
os.environ["TT_MODULES_PATH"] = "E:/sandbox/tech_local/modules.yaml"

if "teamto" not in sys.modules or "srv-bin/scripts/modules" not in sys.modules["teamto"].__path__[0]:
    baseDir = "/mnt/" if platform.os.name == "posix" else "//"
    sys.path.append(baseDir + "srv-bin/scripts/modules")

from teamto.ttImport import ttImport
from opac.core import Server
from opac.helpers import autoConnect, connect, getProject
from opac.models import Asset, Step, Task, File
from opac.utils.fileManagement import FileManagement
from opac import __version__ as opac_version
from jad_pipe.core.context import Context
from jad_pipe.core.pipe import Pipe


config = {
    "API_HOST": "api.ovm.io",
    "API_HTTPS": True,
}

a = autoConnect(config)
proj = getProject(project)
dir_path = os.path.dirname(__file__)
tmp_path = dir_path + "\\temp\\"
logger = logging.getLogger(__name__)
logger.debug("Opac Version : %s", opac_version)
logger.info("[Start]")


def saveFileJSON(elt, filename):
    logger.info("[Save to %s]", filename)
    with open(tmp_path + filename + ".json", "w") as jsonFile:
        json.dump(elt, jsonFile)


def loadfileJSON(filename):
    logger.info("[Load from %s]", filename)
    with open(tmp_path + filename + ".json", "r") as jsonFile:
        return json.load(jsonFile)


#  ===================================
#  Logging
#  ===================================


def jsonprint(elt, sort_keys=False):
    logger.debug(json.dumps(elt, indent=2, sort_keys=sort_keys))


#  =====================================
#  Helper Functions
#  =====================================


saveFileJSON(["hello"], "temp")
hello = loadfileJSON("temp")
jsonprint(hello)
os.remove(tmp_path + "temp" + ".json")
