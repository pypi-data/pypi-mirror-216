from clld.db.meta import Base
from clld.db.models.common import IdNameDescriptionMixin
from sqlalchemy import JSON
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_document_plugin.interfaces import IDocument
from clld_document_plugin.interfaces import ITopic


@implementer(IDocument)
class Document(Base, IdNameDescriptionMixin):
    chapter_no = Column(Integer)
    order = Column(String)

    following_pk = Column(Integer, ForeignKey("document.pk"))
    preceding_pk = Column(Integer, ForeignKey("document.pk"))
    preceding = relationship(
        "Document",
        innerjoin=True,
        foreign_keys=preceding_pk,
        uselist=False,
        remote_side="Document.pk",
        backref="following",
    )

    kind = Column(String, default="chapter")
    meta_data = Column(JSON)

    def __str__(self):
        if not self.chapter_no:
            return self.name
        return f"{self.chapter_no}. {self.name}"


@implementer(ITopic)
class Topic(Base, IdNameDescriptionMixin):
    pass


class TopicDocument(Base):
    topic_pk = Column(Integer, ForeignKey("topic.pk"), nullable=False)
    document_pk = Column(Integer, ForeignKey("document.pk"), nullable=False)
    topic = relationship(Topic, innerjoin=True, backref="references")
    document = relationship(Document, innerjoin=True, backref="references")
    section = Column(String)
    label = Column(String)
