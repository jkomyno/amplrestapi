import confuse


class Config:
    """
    Object used to retrieve configuration variables.
    """

    config = confuse.Configuration('amplrestapi', __name__)

    @classmethod
    def version(cls):
        """
        :return: Project version
        """
        return cls.config['version'].get()

    @classmethod
    def host(cls):
        """"
        :return: IP of the server
        """
        return cls.config['app']['host'].get()

    @classmethod
    def port(cls):
        """"
        :return: Port exposed by the REST server
        """
        return cls.config['app']['port'].get()
