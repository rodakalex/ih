# safe_send.py
import logging
from functools import wraps

from aiogram.types import Message
from aiogram.client.bot import Bot
from aiogram.exceptions import TelegramForbiddenError

def _wrap_method(owner, method_name, logger):
    """Оборачивает owner.method_name и глотает TelegramForbiddenError."""
    if not hasattr(owner, method_name):
        return

    original = getattr(owner, method_name)

    @wraps(original)
    async def wrapped(self, *args, **kwargs):
        try:
            return await original(self, *args, **kwargs)
        except TelegramForbiddenError as e:
            user_id = None
            chat_id = None

            # Для Message.* попытаемся вытащить user/chat
            if isinstance(self, Message):
                user_id = getattr(getattr(self, "from_user", None), "id", None)
                chat_id = getattr(getattr(self, "chat", None), "id", None)
            # Для Bot.send_* первый позиционный аргумент — chat_id
            elif isinstance(self, Bot) and args:
                chat_id = args[0]

            logger.warning(
                "Forbidden in %s: chat_id=%s user_id=%s; %s",
                f"{owner.__name__}.{method_name}",
                chat_id,
                user_id,
                str(e),
            )
            # Возвращаем None, чтобы хэндлер не падал
            return None

    setattr(owner, method_name, wrapped)


def patch_aiogram_senders(logger: logging.Logger | None = None, patch_bot_send_all: bool = True):
    """
    Патчит безопасно:
      - Message.answer / Message.reply (всегда)
      - Любые Bot.send_* (опционально, по умолчанию — да)
    """
    logger = logger or logging.getLogger("safe_send")

    # 1) Самые частые точки — методы Message
    for name in ("answer", "reply"):
        _wrap_method(Message, name, logger)

    # 2) Дополнительно — все методы Bot, начинающиеся с send_
    if patch_bot_send_all:
        for name in dir(Bot):
            if name.startswith("send_") and callable(getattr(Bot, name)):
                _wrap_method(Bot, name, logger)
