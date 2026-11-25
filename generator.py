import random
from faker import Faker
from models import Daycare, Person, Pet

def generate_daycares(n: int, locale: str = "hu_HU", unique: bool = False,
                      min_fee: int = 4000, max_fee: int = 12000) -> list[Daycare]:
    assert n > 0
    assert 0 <= min_fee <= max_fee

    fake = Faker(locale)
    generator = fake if not unique else fake.unique
    prefixes = ["Bundás", "Mancs", "Vidám Tappancs", "Bolondos", "Napsugár", "Csóváló", "Doromboló", "Bársonytalp"]
    suffixes = ["Kisállat Napközi", "Kutya-Macska Óvoda", "Állatpanzió", "Napközi", "Kisállat Megőrző"]

    daycares = []
    for i in range(n):
        city = generator.city()
        name = f"{city}i {random.choice(prefixes)} {random.choice(suffixes)}"
        daycares.append(Daycare(
            "D-" + str(i).zfill(4),
            name,
            city,
            random.randint(min_fee // 500, max_fee // 500) * 500
        ))

    return daycares

def generate_people(n: int, daycares: list[Daycare], male_ratio: float = 0.5, locale: str = "hu_HU",
                    unique: bool = False, min_age: int = 18, max_age: int = 70) -> list[Person]:
    assert n > 0
    assert len(daycares) > 0
    assert 0 < male_ratio < 1
    assert 0 <= min_age <= max_age

    fake = Faker(locale)
    generator = fake if not unique else fake.unique

    people = []
    for i in range(n):
        male = random.random() < male_ratio
        last_name = fake.last_name()
        first_name = generator.first_name_male() if male else generator.first_name_female()
        full_name = f"{last_name} {first_name}"
        chosen_daycare = random.choice(daycares)

        people.append(Person(
            "O-" + str(i).zfill(6),
            full_name,
            random.randint(min_age, max_age),
            male,
            chosen_daycare.id
        ))

    return people

def generate_pets(n: int, owners: list[Person], dog_ratio: float = 0.6,
                  min_age: int = 1, max_age: int = 14) -> list[Pet]:
    assert n > 0
    assert len(owners) > 0
    assert 0 < dog_ratio < 1
    assert 0 <= min_age <= max_age

    dog_names = ["Buksi", "Morzsi", "Bodri", "Rex", "Bella", "Max", "Luna", "Mázli", "Kókusz", "Zeusz", "Bogi", "Fickó"]
    cat_names = ["Cirmi", "Cirmos", "Folti", "Mici", "Füles", "Gombóc", "Loki", "Néró", "Pöttyös", "Masni", "Garfield", "Mirci"]

    pets = []
    for i in range(n):
        is_dog = random.random() < dog_ratio
        species = "kutya" if is_dog else "macska"
        pet_name = random.choice(dog_names if is_dog else cat_names)
        chosen_owner = random.choice(owners)

        pets.append(Pet(
            "P-" + str(i).zfill(6),
            pet_name,
            species,
            random.randint(min_age, max_age),
            chosen_owner.id
        ))

    return pets