import traceback


class WebException(Exception):
    status_code: int = 500

    def __init__(self, *args: object, **kwargs) -> None:
        super().__init__(*args)

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._payload_keys = list(kwargs.keys())

        # self._payload = kwargs

    def dict(self) -> dict:
        return dict(
            error_class=self.__class__.__name__,
            error_message=str(self),
            error_status_code=self.status_code,
            error_traceback=traceback.format_exc(),
            error_payload={k: getattr(self, k) for k in self._payload_keys}
        )
