from pydantic import BaseSettings


class SettingLocal(BaseSettings):
    """
    Settings class for the local environment.
    """

    # Default values for configuration options
    USERNAME_: str = 'myuser'
    PASSWORD: str = '090899'
    HOST: str = 'localhost'
    DATABASE: str = 'jscan'
    PORT: str = '5432'


class SettingDev(BaseSettings):
    """
    Settings class for the development environment.
    """

    # Default values for configuration options
    USERNAME_: str = 'jsadmin'
    PASSWORD: str = 'Pn7mG@6Yp5bz~'
    HOST: str = '3.1.11.181'
    DATABASE: str = 'justscan'
    PORT: str = '17654'
