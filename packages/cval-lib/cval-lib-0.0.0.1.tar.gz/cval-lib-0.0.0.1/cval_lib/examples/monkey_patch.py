from cval_lib.connection import CVALConnection

if __name__ == '__main__':
    api_key = '1d770d0b3f5898ec9e24c5422480b2419b9363852fc14a2e8881de2c6e43b82a'
    cval = CVALConnection(api_key)
    ds = cval.dataset()
    ds.create()
    ds.result.get_results()
