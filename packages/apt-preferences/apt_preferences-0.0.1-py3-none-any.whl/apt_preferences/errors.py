class NoPreferencesFound(ValueError):
    """Unable to find any preference"""

    def __init__(self, file_path=None):
        if file_path is not None:
            self.file_path = file_path

        super().__init__(file_path)
