"""SqliteHandler manages Sqlite connection."""
import sqlite3


class SqliteHandler():
    """Short summary.

    Parameters
    ----------
    conn : str
        Description of parameter `sqlite_db_path`.

    """

    def __init__(self, sqlite_db: str):
        """Short summary.

        Parameters
        ----------
        sqlite_db : str
            Description of parameter `sqlite_db_path`.

        """
        self.conn = sqlite3.Connection(sqlite_db)

    def get_cursor(self):
        """Short summary.

        Parameters
        ----------


        Returns
        -------
        sqlite3.Cursor
            Description of returned object.

        """
        return self.conn.cursor()
