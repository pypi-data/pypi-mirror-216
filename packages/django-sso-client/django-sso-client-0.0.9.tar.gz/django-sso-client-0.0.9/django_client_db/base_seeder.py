from abc import ABC, abstractmethod
import os
import importlib
from django_utils.logger_app import get_logger

class BaseSeeder(ABC):
    
    def __init__(self):
        self.logger = get_logger('BaseSeeder')
    
    @abstractmethod
    def run(self):
        pass

    def create_or_update(self, model, unique_field, unique_value, **defaults):
        unique_field_kwargs = {unique_field: unique_value}
        unique_field_kwargs.update(defaults)
        obj, created = model.objects.get_or_create(**unique_field_kwargs)
        if not created:
            self.logger.info(f"{self.__class__.__name__}: {model.__name__} with {unique_field} {unique_value} existing in the database.")
        else:
            self.logger.info(f"{self.__class__.__name__}: {model.__name__} with {unique_field} {unique_value} successfully created.")
        return obj, created

    @classmethod
    def run_all_seeders(cls, module_name):
        for filename in os.listdir(os.path.dirname(__file__)):
            if filename == "base_seeder.py" or not filename.endswith(".py"):
                continue

            module = importlib.import_module(f"{module_name}.{filename[:-3]}")
            seeder_class = None

            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BaseSeeder) and obj is not cls:
                    seeder_class = obj
                    break

            if seeder_class:
                seeder = seeder_class()
                seeder.run()

    @classmethod
    def run_specific_seeders(cls, module_name, seeder_filenames):
        for filename in seeder_filenames:
            module = importlib.import_module(f"{module_name}.{filename}")
            seeder_class = None

            for name, obj in module.__dict__.items():
                if isinstance(obj, type) and issubclass(obj, BaseSeeder) and obj is not cls:
                    seeder_class = obj
                    break

            if seeder_class:
                seeder = seeder_class()
                seeder.run()