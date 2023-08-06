import sqlalchemy
import transaction
import zope.sqlalchemy
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from clld_document_plugin.models import Document


def load_session(uri):
    DBSession = scoped_session(sessionmaker())
    zope.sqlalchemy.register(DBSession)
    DBSession.configure(bind=sqlalchemy.create_engine(uri))
    return DBSession


def add_documents(uri, chapters):
    DBSession = load_session(uri)
    _add_documents(chapters, DBSession)


def refresh_documents(uri, chapters):
    DBSession = load_session(uri)
    DBSession.query(Document).delete()
    _add_documents(chapters, DBSession)


def _add_documents(chapters, DBSession):
    previous = None
    for chapter in chapters:
        doc = Document(
            chapter["ID"],
            id=chapter["ID"],
            name=chapter["Name"],
            description=chapter["Description"],
            chapter_no=int(chapter["Number"]),
            order=chr(int(chapter["Number"]) + 96),
        )
        if doc.chapter_no > 1:
            doc.preceding = previous

        previous = doc
        DBSession.add(doc)

    transaction.commit()
    transaction.begin()
