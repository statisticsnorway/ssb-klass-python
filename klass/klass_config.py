class Singleton():
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.singleton_init(*args, **kwds)
        return it


class KlassConfig(Singleton):
    def singleton_init(self):
        self.LANGUAGES = ["nb", "nn", "en"]
        self.BASE_URL = "https://data.ssb.no/api/klass/v1/"
        self.HEADERS = {
            "Accept": 'application/json',
        }
        self.TESTING = False
