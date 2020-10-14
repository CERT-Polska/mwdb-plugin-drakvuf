import logging
import requests

from mwdb.core.plugins import PluginAppContext, PluginHookHandler
from mwdb.model import db, File, MetakeyDefinition

from .config import config


logger = logging.getLogger("mwdb.plugin.drakvuf")


class DrakvufHookHandler(PluginHookHandler):
    def on_created_file(self, file: File):
        """
        Create Drakvuf Sandbox job for newly added file.
        Add analysis identifier as 'drakvuf' attribute.
        """
        if not file.file_type.startswith("PE32 executable"):
            logger.debug("Not a PE executable, ignoring.")
            return

        # Get contents path from "uploads" directory
        contents_path = file.get_path()
        # Send request to Drakvuf Sandbox
        req = requests.post(f"{config.drakvuf.drakvuf_url}/upload", files={
            "file": (file.sha256 + ".exe", open(contents_path, "rb")),
        }, data={
            "timeout": config.drakvuf.timeout
        })
        req.raise_for_status()
        # Get task identifier
        task_uid = req.json()["task_uid"]
        # Add it as attribute to the file
        file.add_metakey("drakvuf", task_uid, check_permissions=False)
        logger.info("File sent to Drakvuf. Analysis identifier: %s", task_uid)


def entrypoint(app_context: PluginAppContext):
    """
    Register plugin hook handler.

    This will be called on app load.
    """
    app_context.register_hook_handler(DrakvufHookHandler)


def configure():
    """
    Configure 'drakvuf' attribute key in MWDB.

    This will be called by 'mwdb configure' command.
    """
    logger.info("Configuring 'drakvuf' attribute key.")
    attribute = MetakeyDefinition(key="drakvuf",
                                  url_template=f"{config.drakvuf.drakvuf_url}/progress/$value",
                                  label="Drakvuf analysis",
                                  description="Reference to the Drakvuf analysis for file")
    db.session.merge(attribute)
    db.session.commit()
