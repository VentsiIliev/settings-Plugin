from typing import Protocol


class RobotSettingsService(Protocol):

    def load_config(self):
        ...

    def save_config(self, config):
        ...

    def load_calibration(self):
        ...

    def save_calibration(self, calibration):
        ...