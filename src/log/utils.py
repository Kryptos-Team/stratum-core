import platform


def is_supported():
    """Checks whether operating system supports main symbols"""
    os_arch = platform.system()

    if os_arch != "Windows":
        return True

    return False
