import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class TLS12Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Chỉ sử dụng TLS 1.2+
        kwargs['ssl_context'] = ctx
        return super(TLS12Adapter, self).init_poolmanager(*args, **kwargs)