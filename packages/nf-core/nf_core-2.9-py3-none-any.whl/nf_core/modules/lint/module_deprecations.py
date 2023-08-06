import logging
import os

log = logging.getLogger(__name__)


def module_deprecations(_, module):
    """
    Check that the modules are up to the latest nf-core standard
    """
    module.wf_path = module.module_dir
    if "functions.nf" in os.listdir(module.module_dir):
        module.failed.append(
            (
                "module_deprecations",
                "Deprecated file `functions.nf` found. No longer required for the latest nf-core/modules syntax!",
                module.module_dir,
            )
        )
