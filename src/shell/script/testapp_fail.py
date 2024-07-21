from src.common.logger import LOGGER
from src.common import ssd_config
from src.shell.script import TestAppBase, ReturnObject


class TestApp(TestAppBase):
    def main(self):
        self.read(0)
        is_mismatched = True
        # Always Result Fail Return
        if not is_mismatched:
            LOGGER.debug("Test Success")
            return ReturnObject(0, None)
        else:
            LOGGER.debug("Test Fail Return")
            return ReturnObject(-1, None)
def main():
    app = TestApp()
    return app.main()
