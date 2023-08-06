from urllib.parse import urljoin

from requests import Session

from pytest_smtp4dev.models import MessageIdModel, MessagesModel


class Smtp4devClient:
    def __init__(self, base_url: str, /) -> None:
        self.session = Session()
        self.base_url = base_url

    @property
    def total_messages(self) -> int:
        messages = self.get_messages()
        return messages.row_count

    def get_messages(self, /, *, page: int = 1, size: int = 50) -> MessagesModel:
        params = {
            'sortColumn': 'receivedDate',
            'sortIsDescending': True,
            'page': page,
            'size': size,
        }

        response = self.session.get(
            url=urljoin(self.base_url, '/api/Messages'),
            params=params,
        )
        return MessagesModel.parse_obj(response.json())

    def get_message_by_id(self, message_id: str, /) -> MessageIdModel:
        response = self.session.get(url=urljoin(self.base_url, f'/api/Messages/{message_id}'))
        response_html = self.session.get(url=urljoin(self.base_url, f'/api/Messages/{message_id}/html'))
        model = MessageIdModel.parse_obj(response.json())
        model.raw_html = response_html.text
        return model

    def get_messages_by_rcpt_to(self, rcpt_to: str, /) -> list[MessageIdModel]:
        messages = []
        for message_id in [m.id for m in self.get_messages(page=1, size=self.total_messages).results or []]:
            message_object = self.get_message_by_id(message_id)
            if message_object.rcpt_to == rcpt_to:
                messages.append(message_object)
        return messages
