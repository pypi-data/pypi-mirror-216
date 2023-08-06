import logging
import sys

# need to import interfaces to register them in registry for loading
# TODO: automatize implicitly
from scida.convenience import load
from scida.customs.arepo.dataset import ArepoSnapshot
from scida.customs.arepo.series import ArepoSimulation
from scida.interfaces.gadgetstyle import GadgetStyleSnapshot

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
