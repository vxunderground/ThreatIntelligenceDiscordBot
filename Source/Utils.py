import logging

def get_missing_config_params(config, section_name):
    return [
        detail_name for detail_name, detail in config.items(section_name) if not detail
    ]


def verify_config_section(config, section_name):
    return section_name in config and all(
        [detail for detail_name, detail in config.items(section_name)]
    )

def configure_logger(name: str = __name__) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_handlers = {
        "printHandler": {"logger": logging.StreamHandler(), "level": logging.DEBUG},
        "fileHandler": {
            "logger": logging.FileHandler(f"logs/{name}.info.log"),
            "level": logging.INFO,
        },
        "errorHandler": {
            "logger": logging.FileHandler(f"logs/{name}.error.log"),
            "level": logging.ERROR,
        },
    }

    logger_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    for handler_name in log_handlers:
        log_handlers[handler_name]["logger"].setLevel(
            log_handlers[handler_name]["level"]
        )
        log_handlers[handler_name]["logger"].setFormatter(logger_format)
        logger.addHandler(log_handlers[handler_name]["logger"])

    return logger
