import yaml

import yaml

def load_config(config_file, app):
    """
    Loads the application configuration from a YAML file, validates its contents,
    and sets default values for missing configuration settings.

    The function ensures that essential configuration settings such as window settings,
    update interval, and chroma key settings have valid values. If specific settings
    are missing from the configuration file, default values are assigned to guarantee
    the application's functionality.

    Args:
        config_file (str): The path to the YAML configuration file.
        app (QApplication): The main application.

    Returns:
        dict: The loaded and validated configuration with default values for missing settings.
    """
    # Load the configuration file
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # Validate and set defaults for window_settings
    window_settings = config.get('window_settings', {})
    window_settings['title'] = window_settings.get('title', 'Unassigned Window')
    window_settings['size'] = window_settings.get('size', {'width': 800, 'height': 600})
    window_settings['position'] = window_settings.get('position', {'x': 100, 'y': 100})

    # Validate and set defaults for update_interval
    config['update_interval'] = config.get('update_interval', 70)

    # Validate and set defaults for chroma_key_settings
    chroma_key_settings = config.get('chroma_key_settings', {})
    chroma_key_settings['hsv_lower'] = chroma_key_settings.get('hsv_lower', {'h': 50, 's': 100, 'v': 100})
    chroma_key_settings['hsv_upper'] = chroma_key_settings.get('hsv_upper', {'h': 70, 's': 255, 'v': 255})

    # Validate and set defaults for selected_screen
    config['selected_screen'] = config.get('selected_screen', app.primaryScreen().name())

    # Reassign validated and defaulted settings back to config
    config['window_settings'] = window_settings
    config['chroma_key_settings'] = chroma_key_settings

    return config
