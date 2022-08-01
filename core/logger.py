from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "ml_workflow": {
            "propagate": False,
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}


def configure_logger(incoming_log_config):
    for logger in incoming_log_config:
        if logger not in logging_config["loggers"]:
            logging_config["loggers"][logger] = incoming_log_config[logger]
        else:
            for config in incoming_log_config[logger]:
                logging_config["loggers"][logger][config] = incoming_log_config[logger][
                    config
                ]

    dictConfig(logging_config)
