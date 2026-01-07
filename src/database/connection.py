import mysql.connector
from mysql.connector import Error
import configparser
import os

class DbConnection:
    """
    Singleton class responsible for managing
     the database connection lifecycle.
    """
    _instance = None

    def __init__(self):
        """
        Initializes the configuration loader.
        """
        self._conn = None
        self._config = self._load_config()

    def _load_config(self):
        """
        Internal method to locate and parse the 'config.ini' file.
        :return: config.
        """
        config = configparser.ConfigParser()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_path = os.path.join(base_dir, 'config', 'config.ini')

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file doesnt exist: {config_path}")

        config.read(config_path)
        return config

    def connect(self):
        """
        Establishes or retrieves the existing database connection.
        using credentials from the configuration.
        :return: Connection object
        """
        if self._conn is None or not self._conn.is_connected():
            try:
                db_conf = self._config['database']

                if not db_conf['database']:
                    raise ValueError("Check the configuration file and fix the database connection.")
                if not db_conf['port']:
                    raise ValueError("Check the configuration file and fix the database connection.")
                if not db_conf['host']:
                    raise ValueError("Check the configuration file and fix the database connection.")
                if not db_conf['user']:
                    raise ValueError("Check the configuration file and fix the database connection.")

                self._conn = mysql.connector.connect(
                    host=db_conf['host'],
                    user=db_conf['user'],
                    password=db_conf.get('password', ''),
                    database=db_conf['database'],
                    port=int(db_conf.get('port',''))
                )

            except Error as e:
                self._conn = None
                raise e
        return self._conn

    def close(self):
        """
        Safely closes the active database
         connection if it is currently open.
        """
        if self._conn is not None and self._conn.is_connected():
            self._conn.close()
            print("Session end.")

    @staticmethod
    def get_instance():
        """
        Static access method for the Singleton instance.
        Creates the instance.
        :return: DbConnection instance
        """
        if DbConnection._instance is None:
            DbConnection._instance = DbConnection()
        return DbConnection._instance