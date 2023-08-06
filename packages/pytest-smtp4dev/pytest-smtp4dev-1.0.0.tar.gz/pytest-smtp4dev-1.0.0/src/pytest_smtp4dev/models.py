import os
import typing as t
from datetime import datetime
from urllib.parse import urljoin

import requests
from PIL import Image
from pydantic.main import BaseModel, Field


######################
# /api/Messages/{id} #
######################
class MessageIdHeaderModel(BaseModel):
    name: str = Field(alias='name')
    value: str = Field(alias='value')


class MessageIdPartAttachmentModel(BaseModel):
    file_name: str = Field(alias='fileName')
    id: str = Field(alias='id')
    url: str = Field(alias='url')


class MessageIdPartModel(BaseModel):
    attachments: list[MessageIdPartAttachmentModel] = Field(alias='attachments')
    name: str = Field('name')
    size: int = Field('size')


class MessageIdModel(BaseModel):
    id: str = Field(alias="id")
    bcc: str = Field(alias="bcc")
    cc: str = Field(alias="cc")
    headers: list[MessageIdHeaderModel] = Field(alias='headers')
    subject: str = Field(alias="subject")
    mail_from: str = Field(alias="from")
    rcpt_to: str = Field(alias='to')
    received_date: datetime = Field(alias='receivedDate')
    mime_parse_error: t.Optional[str] = Field(alias='mimeParseError')
    parts: list[MessageIdPartModel] = Field('parts')
    raw_html: t.Optional[str] = Field()

    def get_attachments(self) -> dict[str, Image]:
        if len(self.parts) > 0:
            return {
                attachment.file_name: Image.open(
                    requests.get(urljoin(os.getenv('SMTP4DEV_HOSTNAME'), attachment.url), stream=True).raw,
                )
                for attachment in self.parts[0].attachments
            }
        return {}


#################
# /api/Messages #
#################
class MessagesOneModel(BaseModel):
    id: str = Field(alias='id')

    class Config:
        allow_population_by_field_name = True


class MessagesModel(BaseModel):
    results: list[MessagesOneModel] = Field(alias='results')
    row_count: int = Field(alias='rowCount')

    class Config:
        allow_population_by_field_name = True

    def is_empty(self) -> bool:
        return len(self.results) == 0
