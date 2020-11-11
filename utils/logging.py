import logging

from utils import PROFILE_LOG_LEVEL

logging.addLevelName(PROFILE_LOG_LEVEL, "PROFILE")


def profile(self, message, *args, **kws):
    if self.isEnabledFor(PROFILE_LOG_LEVEL):
        self._log(PROFILE_LOG_LEVEL, message, args, **kws)


logging.Logger.profile = profile
data_downloader_logger = logging.getLogger("DataDownloader")
get_stat_logger = logging.getLogger("GetStat")
