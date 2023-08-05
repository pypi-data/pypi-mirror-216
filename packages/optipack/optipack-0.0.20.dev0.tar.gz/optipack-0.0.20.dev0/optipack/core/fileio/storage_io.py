from abc import ABC, abstractmethod
from optipack.sdk.optipack_logger import OptipackLogger
from typing import List, Dict, Any
from PIL.Image import Image
try: 
    from typing import Self
except:
    from typing_extensions import Self

logger = OptipackLogger(name='opt-store-logger', log_dir='.otp_log')

class Storage(ABC):
    def __new__(cls: type[Self],
                storage_name: str,
                storage_cfg_dir: str = '',
                **kwargs
                ) -> Self:
        storage_mapper = dict(
            mongodb=MongoDBStore,
            minio=MinioStore, 
            gcs = GCStore,
            gcsfs = GCSFS
        )
        if storage_cfg_dir: 
            logger.info(f'Config will be loaded from directory {storage_cfg_dir}')
            kwargs = dict(cfg_dir = storage_cfg_dir)
        else:
            logger.warning('Config directory is not provided, checking kwargs')
            if not kwargs or None in kwargs.values(): 
                raise RuntimeError('Neither directory nor kwargs are provided. Ending creating object...')

        if cls is Storage:
            StorageCls = storage_mapper.get(storage_name, None)
            assert StorageCls, 'Invalid storage class'
            logger.info(f'Creating storage {StorageCls}')
            return super(Storage, cls).__new__(StorageCls)
        return super(Storage, cls).__new__(cls, storage_name, storage_cfg_dir, **kwargs)

    def __init__(self, 
                 storage_name: str, 
                 **kwargs
                 ) -> None:
        self.__name__ = storage_name
        
        cfg = kwargs
        if 'cfg_dir' in kwargs: 
            try: 
                from optipack.core.fileio.reader_misc import read_yaml
                cfg = read_yaml(kwargs['cfg_dir'])
            except Exception as e: 
                logger.error(f'Error {e} happenned while attempt reading configuration from {kwargs["cfg_dir"]}')
                return None

        for k in cfg: 
            setattr(self, k, cfg[k])

    @abstractmethod
    def _validate(self): 
        pass

    @abstractmethod
    def _connect(self): 
        pass

    @abstractmethod
    def write_json(self): 
        pass

    @abstractmethod
    def view(self): 
        pass

    # @abstractmethod
    # def write(self):
    #     pass

class MongoDBStore(Storage):
    def __init__(self, storage_name: str, **kwargs) -> None:
        super().__init__(storage_name, **kwargs)
        self._validate()
        self.connection_string = f'mongodb://{self.username}:{self.password}@{self.host}/{self.db_name}/'
        self._connect()
        if self.db_name: 
            self.get_database(self.db_name)
        if self.db and self.collection_name: 
            self.get_collection(self.collection_name)

    def _validate(self):
        return super()._validate()

    def _connect(self, connect_str = ''):
        try: 
            from pymongo import MongoClient
            if not connect_str: 
                connect_str = self.connection_string
            self.client = MongoClient(connect_str)
        except Exception as e: 
            logger.info(f'Error {e} happened while connecting to MongoDB')
            raise e

    def get_database(self, db_name: str):
        try: 
            db = self.client[db_name]
            assert db, 'Invalid database'
            self.db = db
        except Exception as e: 
            logger.error(f'Error {e} happened while getting database')
            raise e 

    def get_collection(self, collection_name: str):
        try: 
            if not self.db: 
                raise AttributeError('Database not found')
            collection = self.db[collection_name]
            assert collection, 'Invalid collection'
            self.collection = collection
        except Exception as e: 
            logger.error(f'Error {e} happened while retrieving collection name {collection_name}')

    def write_json(self, items:list):
        # format of mongodb item. TODO: add checking keys
            # _id (mongodb's object id)
            # key: user define unique key 
            # other attributes
        try: 
            assert items, 'Empty items'
            inserted = self.collection.insert_many(items)
            return inserted
        except Exception as e: 
            logger.info(f'Error {e} happend while trying to insert {items} to {self.collection}')
            raise e

    def view(self):
        return super().view()

class MinioStore(Storage):
    def __init__(self, storage_name: str, **kwargs) -> None:
        try:
            super().__init__(storage_name=storage_name, **kwargs)
            self._validate()
            self._connect()
        except Exception as e: 
            raise e

    def _validate(self):
        return super()._validate()

    def _connect(self):
        from fs_miniofs import MINIOFS
        try: 
            self.fs = MINIOFS(
                endpoint_url= self.url, 
                bucket_name= self.bucket, 
                aws_access_key_id = self.username, 
                aws_secret_access_key = self.password,
            )
            assert self.fs, 'Cannot connect to minio'
        except Exception as e: 
            logger.error(f'Error {e} happened when attempting connect to minio using')
            logger.info(f'URL: {self.url}')
            logger.info(f'Bucket: {self.bucket}')
        
    
    def write_json(self, fpath: str, content: dict):
        import json
        try: 
            self.fs.writetext(fpath, json.dumps(content))
        except Exception as e: 
            logger.error(f'Error {e} happened when writing to {fpath}') 
            raise e
        
    def write_image(self, fpath: str, image: Image): 
        try:
            with self.fs.open(fpath, 'wb') as f: 
                image.save(f)
            logger.info(f'Image sucessfully saved to {fpath}')
        except Exception as e:
            logger.error(e)
            raise e

    def view(self):
        return super().view()

class GCStore(Storage): 
    def __init__(self, storage_name: str, **kwargs) -> None:
        super().__init__(storage_name, **kwargs)

    def _validate(self):
        return super()._validate()
    
    def _connect(self):
        return super()._connect()
    
    def write(self):
        ...

    #TODO: to be implemented

class GCSFS(Storage):
    def __init__(self, storage_name: str, **kwargs) -> None:
        super().__init__(storage_name, **kwargs)
        self._validate()
        self._connect()
        
    def _validate(self):
        return super()._validate()

    def _connect(self):
        try:
            import fs_gcsfs
            self.fs = fs_gcsfs.GCSFS(bucket_name= self.bucket)
        except Exception as e:
            logger.error(f'Error {e} happened when initialize with bucket {self.bucket}') 
            raise e
    
    def write_json(self, path: str, content: dict):
        import json
        try: 
            with self.fs.open(path, 'w') as f:
                f.write(json.dumps(content))
            logger.info(f'JSON file successfully saved to {path}')
        except Exception as e:
            logger.error(e)
            raise e

    def write_image(self, path: str, image: Image):
        try:
            with self.fs.open(path, 'wb') as f: 
                image.save(f)
            logger.info(f'Image sucessfully saved to {path}')
        except Exception as e:
            logger.error(e)
            raise e
        
    def write(self):
        return super().write()
    
    def view(self):
        return super().view()
    
    def read_json(self, path)->dict:
        import json
        try:
            with self.fs.open(path) as f: 
                output = json.load(f)
            return output
        except Exception as e:
            logger.error(e)
            raise e

    def read_image(self, path):
        from PIL import Image
        try:
            with self.fs.open(path, 'rb') as f: 
                image = Image.open(f)
                image.load()
            return image
        except Exception as e:
            logger.error(e)
            raise e


if __name__=='__main__': 
    cfg = dict(bucket = 'om-mlops-serving-results-np')

    store = Storage(storage_name='gcsfs', **cfg)
    # store.write_json('test_sdk.json',dict(id='test-sdk'))
    img = store.read_image('0.jpeg')
    print(img)

 