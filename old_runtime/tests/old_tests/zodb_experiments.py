import ZODB, ZODB.FileStorage
import account, BTrees.OOBTree


if __name__ == "__main__":

    storage = ZODB.FileStorage.FileStorage('mydata.fs')
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root



