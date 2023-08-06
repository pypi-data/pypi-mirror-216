from cval_lib.connection import CVALConnection

if __name__ == '__main__':
    # set up your api_key
    api_key = 'a42a3a750b2dfab2f90ef64e75ba99a7c49a6c3f427d762236459d87e6766af1'
    # set up session
    cval = CVALConnection(api_key)
    # choose strategy
    ds = cval.dataset()
    # create your dataset
    ds_id = ds.create()
    print(ds_id)
    # update your dataset
    update = ds.update(name='any')
    print(update)
    # watch changes
    get = ds.get()
    print(get)
    # also you can use dataset_id for watch changes
    get = ds.get(ds_id)
    print(get)
    # get all datasets
    print(ds.get_all())
