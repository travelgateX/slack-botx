import os
import configparser
import logging
import logging.config


class Config:
    """ Get config from config file or environment variables.
    The priority order of config is: Environment > Config file > default_value.
    The env var is composed by: [SECTION]_[OPTION]
    For example:
    get_or_else('smtp', 'BIND_ADDRESS', '127.0.0.1')
    => os.environ.get('SMTP_BIND_ADDRESS', '127.0.0.1')
    """
    config = configparser.ConfigParser()

    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}

    @staticmethod
    def init_config(file='app/config.ini'):
        Config.config.read(file)
        logging.config.fileConfig(file, disable_existing_loggers=False)   # init logger
           
    @staticmethod
    def get_or_else(section, option, default_value):
        ret = os.environ.get('_'.join([section.upper(), option]))
        if ret is None:
            ret = Config.config.get(section, option, fallback=default_value)
        return ret    

    @staticmethod
    def getint_or_else(section, option, default_value):
        ret = Config._get_conv_env_or_else(section, option,int,None)
        if ret is None:
            ret = Config.config.getint(section, option,fallback=default_value)
        return ret

    @staticmethod
    def getfloat_or_else(section, option, default_value):
        ret = Config._get_conv_env_or_else(section, option,float, None)
        if ret is None:
            ret = Config.config.getfloat(section, option,fallback=default_value)
        return ret
        
    @staticmethod
    def getboolean_or_else(section, option, default_value):
        ret = Config._get_conv_env_or_else(section, option,Config._convert_to_boolean, None)
        if ret is None:
            ret = Config.config.getboolean(section, option,fallback=default_value)
        return ret

    @staticmethod
    def _get_conv_env_or_else(section, option, conv, default_value):
        return conv(os.environ.get('_'.join([section.upper(), option.upper()]),
                                   default_value))

    @staticmethod
    def _convert_to_boolean(value):
        """Return a boolean value translating from other types if necessary.
        """
        if value.lower() not in Config.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return Config.BOOLEAN_STATES[value.lower()]