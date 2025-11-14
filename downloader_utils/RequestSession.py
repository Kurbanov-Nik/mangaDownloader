from abc import ABC, abstractmethod

class RequestSession(ABC):
    statusCodes = {
        200: ("OK", "Доступ к ресурсу разрешен"),
        302: ("Found", "Ресурс перенаправляет по другому URL"),
        304: ("Not Modified", ""),
        400: ("Bad Request", "Не корректный запрос к ресурсу"),
        401: ("Unauthorized", "Требуется аутентификация"),
        403: ("Forbidden", "Нет прав доступа к ресурсу"),
        404: ("Not Found", "Ресурс не найден"),
        429: ("Too Many Requests", "Слишком много запросов"),
        500: ("Internal Server Error", "Непредвиденная ошибка на стороне сервера"),
        502: ("Bad Gateway", "Соединение разорвано"),
        503: ("Service Unavailable", "Ресурс временно недоступен"),
        504: ("Gateway Timeout", "Ожидание ответа прервано"),
        505: ("HTTP Version Not Supported", "HTTP подключение не поддерживается")
    }

    @abstractmethod
    def __init__(self):
        self.userAgent = None

    @abstractmethod
    def testRequest(self):
        ...

    @abstractmethod
    def collectMangaInfo(self):
        ...

    @abstractmethod
    def collectChapters(self):
        ...

    def setUserAgent(self, agent):
        self.userAgent = agent