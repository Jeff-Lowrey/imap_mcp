import logging
import re


class MCP_Logger:
    def __init__(self, config_dict):
        self.logging_config = config_dict
        self.logging_config = {
            "version": 1,
            "filters": {
                "mask_filter": {
                    "()": SensitiveDataFilter,
                    "param": "noshow",
                }
            },
            "handlers": {"console": {"class": "logging.StreamHandler", "filters": ["myfilter"]}},
            "root": {"level": "DEBUG", "handlers": ["console"]},
        }


class SensitiveDataFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        # TODO: Replace with retrieval from config, or set in some other method with keys identified from config
        self.sensitive_keys = ["password", "api_key", "spf_record"]

    def filter(self, record):
        try:
            record.msg = self.mask_sensitive_msg(record.msg)
            return True
        except Exception:
            return True

    def mask_sensitive_msg(self, message):
        # TODO: Figure out how to do this without regex
        # mask sensitive data in multi record.args
        for key in self.sensitive_keys:
            pattern_str = rf"'{key}': '[^']+'"
            replace = f"'{key}': '******'"
            message = re.sub(pattern_str, replace, message)
        return message
