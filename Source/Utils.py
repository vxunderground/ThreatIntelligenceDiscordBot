def get_missing_config_params(config, section_name):
    return [
        detail_name for detail_name, detail in config.items(section_name) if not detail
    ]


def verify_config_section(config, section_name):
    return section_name in config and all(
        [detail for detail_name, detail in config.items(section_name)]
    )
