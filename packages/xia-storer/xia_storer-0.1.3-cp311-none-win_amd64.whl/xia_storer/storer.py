import os


class Storer:
    """Store logging data
    """
    root_location = "."
    supported_stores = []
    default_store = ""
    path_separator = os.path.sep  #: Current OS path seperator

    def __init__(self, location: str, data_store: str = "", **kwargs):
        data_store = data_store if data_store else self.default_store
        if data_store not in self.supported_stores:
            raise ValueError(f"{data_store} is not supported by {self.__class__.__name__}")
        self.data_store = data_store
        self.location = location

    def get_read_fp(self):
        """Get file-like object to ready

        Returns:
            a readable file-like object
        """

    def get_write_fp(self):
        """Get file-like object to write

        Returns:
            a writable file-like object
        """

    @classmethod
    def get_log_location(cls, domain_name: str, model_name: str, address_name: str, start_seq: str):
        dir_path = cls.path_separator.join([cls.root_location, domain_name, model_name, address_name])
        location = cls.path_separator.join([dir_path, start_seq])
        return location


class FileStorer(Storer):
    supported_stores = ["file"]
    default_store = "file"

    def get_read_fp(self):
        """Get file-like object to ready

        Returns:
            a readable file-like object
        """
        if self.data_store == "file":
            file_path = self.location
            with open(file_path, 'rb') as fp:
                yield fp

    def get_write_fp(self):
        """Get file-like object to write

        Returns:
            a writable file-like object
        """
        if self.data_store == "file":
            dir_path = self.path_separator.join(self.location.split(self.path_separator)[:-1])
            if dir_path and dir_path != '.':  # Compatible with current path
                os.makedirs(dir_path, exist_ok=True)
            with open(self.location, 'wb') as fp:
                yield fp
