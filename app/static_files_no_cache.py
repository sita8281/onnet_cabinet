from fastapi.staticfiles import StaticFiles


class StaticNoCache(StaticFiles):
    def is_not_modified(self, *args, **kwargs) -> bool:
        return False

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers["Cache-Control"] = "no-cache"
        return resp