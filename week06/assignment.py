from abc import ABCMeta, abstractmethod
import yaml

with open("config.yaml", "r") as file:
    yamlLoader = yaml.safe_load(file)


animal_size_mapping = yamlLoader["CONFIG"]["AnimalSizeMapping"]
animal_size_threshold = int(yamlLoader["CONFIG"]["AnimalSizeThreshold"])


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def animal_type(self):
        pass

    @abstractmethod
    def size(self):
        pass
    
    @abstractmethod
    def personality(self):
        pass

    @abstractmethod
    def ifFierce(self):
        pass

 
class Cat(Animal):
    sound = "mew"

    def __init__(self, name, animal_type, size, personality, ifFierce, ifPet):
        self._name = name
        self._type = animal_type
        self._size = size
        self._personality = personality
        self._ifFierce = ifFierce
        self._ifPet = ifPet

    def __eq__(self, other): 

        if not isinstance(self, other.__class__):
            return NotImplemented

        return self
    
    @classmethod
    def creator(cls, name, animal_type, size, personality):        
        if animal_size_mapping[size] >= animal_size_threshold and \
        animal_type == "食肉" and \
        personality == "凶猛":
           ifFierce = True
           ifPet = False
        else:
            ifFierce = False
            ifPet = True

        cat = cls(name, animal_type, size, personality, ifFierce, ifPet)

        return cat 

    @property
    def animal_type(self):
        return self._type
    
    @property
    def personality(self):
        return self._personality

    @property
    def size(self):
        return self._size

    @property
    def ifFierce(self):
        return self._ifFierce
    
    @property
    def ifPet(self):
        return self._ifPet

class Dog(Animal):
    sound = "wang"

    def __init__(self, name, animal_type, size, personality, ifFierce, ifPet):
        self._name = name
        self._type = animal_type
        self._size = size
        self._personality = personality
        self._ifFierce = ifFierce
        self._ifPet = ifPet

    def __eq__(self, other): 

        if not isinstance(self, other.__class__):
            return NotImplemented

        return self
    
    @classmethod
    def creator(cls, name, animal_type, size, personality):        
        if animal_size_mapping[size] >= animal_size_threshold and \
        animal_type == "食肉" and \
        personality == "凶猛":
           ifFierce = True
           ifPet = False
        else:
            ifFierce = False
            ifPet = True

        dog = cls(name, animal_type, size, personality, ifFierce, ifPet)

        return dog

    @property
    def animal_type(self):
        return self._type
    
    @property
    def personality(self):
        return self._personality

    @property
    def size(self):
        return self._size

    @property
    def ifFierce(self):
        return self._ifFierce
    
    @property
    def ifPet(self):
        return self._ifPet


class Zoo(object):

    def __init__(self, name):
        self._name = name
        self.animals = []
    
    def add_animal(self, animalName):

        if not hasattr(self, animalName.__class__.__name__):
            setattr(self, animalName.__class__.__name__, None)
        
        if animalName not in self.animals:
            self.animals.append(animalName)


def main():
    z = Zoo("时间动物园")
    cat1 = Cat.creator("大花猫1", "食肉", "大", "凶猛")
    dog1 = Dog.creator("小泰迪", "食肉", "中", "温顺")
    z.add_animal(cat1)
    z.add_animal(dog1)
    have_cat = hasattr(z, "Cat")
    have_dog = hasattr(z, "Dog")
    print(have_cat, have_dog)
    print(dog1.ifFierce, dog1.ifPet)
    print(cat1.ifFierce, cat1.ifPet)

if __name__ == "__main__":
    main() 

