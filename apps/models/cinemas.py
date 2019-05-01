# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text

from apps.common.database import Base


class Cinema(Base):
    __tablename__ = 'cinemas'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    image_url = Column(Text())
    address = Column(String(50))
    detail_address = Column(String(30))

    def __init__(self, title=None, image_url=None, address=None, detail_address=None):
        self.title = title
        self.image_url = image_url
        self.address = address
        self.detail_address = detail_address

    def __repr__(self):
        return '<Cinema {}>'.format(self.id)
