import sqlalchemy

from database import DB

def main():
    db = DB()
    db.connect_database()
    db.init_database()


if __name__ == "__main__":
    main()