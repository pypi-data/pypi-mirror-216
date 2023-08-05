
"""BlueDesc Molecular Descriptor Java Executable."""

import os
from pathlib import Path

__version__ = "2008.10.03"
BLUEDESC_EXEC_PATH = Path(os.path.abspath(os.path.join(__file__, os.pardir, 'ODDescriptors.jar')))
