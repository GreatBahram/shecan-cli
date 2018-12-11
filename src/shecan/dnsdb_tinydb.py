""" Database wrapper for TinyDB for Shecan CLI project."""
from typing import List

import tinydb


class DNSDB_TinyDB():
    """Wrapper class for TinyDB.  """

    def __init__(self, db_path: str) -> None:
        """Connect to db."""
        self._db = tinydb.TinyDB(db_path)

    def add(self, dns: dict) -> int:
        """Add a dns dict to db."""
        dns_id = self._db.insert(dns)
        dns['id'] = dns_id
        self._db.update(dns, doc_ids=[dns_id])
        return dns_id

    def get(self, dns_id: int) -> dict:
        """Return a dns dict with matching id."""
        return self._db.get(doc_id=dns_id)

    def list_dns(self) -> List[dict]:
        """Return list of dns."""
        return self._db.all()

    def count(self) -> int:
        """Return number of dns in db."""
        return len(self._db)

    def update(self, dns_id: int, dns: dict) -> None:
        """Modify dns in db with given dns_id."""
        self._db.update(dns, doc_ids=[dns_id])

    def delete(self, dns_id: int) -> None:
        """Remove a dns from db with given dns_id."""
        self._db.remove(doc_ids=[dns_id])

    def delete_all(self) -> None:
        """Remove all shecan's dns servers from db."""
        self._db.purge()

    def unique_id(self) -> int:
        """Return an integer that does not exist in the db."""
        i = 1
        while self._db.contains(doc_ids=[i]):
            i += 1
        return i

    def stop_dns_db(self) -> None:
        """Disconnect from DB."""
        self._db.close()


def start_dns_db(db_path: str) -> DNSDB_TinyDB:
    """Connect to db."""
    return DNSDB_TinyDB(db_path)
