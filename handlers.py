import csv
import json
import os
import openpyxl
from openpyxl.workbook import Workbook
from models import Daycare, Person, Pet

#json
def write_json(daycares: list[Daycare], people: list[Person], pets: list[Pet], path: str) -> None:
    with open(os.path.join(path, "daycares.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps([d.__dict__ for d in daycares], indent=2, ensure_ascii=False))
    with open(os.path.join(path, "people.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps([p.__dict__ for p in people], indent=2, ensure_ascii=False))
    with open(os.path.join(path, "pets.json"), "w", encoding="utf-8") as f:
        f.write(json.dumps([pet.__dict__ for pet in pets], indent=2, ensure_ascii=False))


def read_json(path: str) -> tuple[list[Daycare], list[Person], list[Pet]]:
    with open(os.path.join(path, "daycares.json"), "r", encoding="utf-8") as f:
        daycares = [Daycare(**row) for row in json.load(f)]
    with open(os.path.join(path, "people.json"), "r", encoding="utf-8") as f:
        people = [Person(**row) for row in json.load(f)]
    with open(os.path.join(path, "pets.json"), "r", encoding="utf-8") as f:
        pets = [Pet(**row) for row in json.load(f)]
    return daycares, people, pets

#csv
def write_csv(daycares: list[Daycare], people: list[Person], pets: list[Pet], path: str, delimiter: str = ";") -> None:
    with open(os.path.join(path, "daycares.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "city", "daily_fee"], delimiter=delimiter)
        writer.writeheader()
        for d in daycares:
            writer.writerow(d.__dict__)

    with open(os.path.join(path, "people.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "age", "gender", "daycare_id"], delimiter=delimiter)
        writer.writeheader()
        for p in people:
            writer.writerow({
                "id": p.id,
                "name": p.name,
                "age": p.age,
                "gender": "férfi" if p.male else "nő",
                "daycare_id": p.daycare_id
            })

    with open(os.path.join(path, "pets.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "species", "age", "owner_id"], delimiter=delimiter)
        writer.writeheader()
        for pet in pets:
            writer.writerow(pet.__dict__)


def read_csv(path: str, delimiter: str = ";") -> tuple[list[Daycare], list[Person], list[Pet]]:
    with open(os.path.join(path, "daycares.csv"), "r", encoding="utf-8") as f:
        daycares = [Daycare(r["id"], r["name"], r["city"], int(r["daily_fee"])) for r in csv.DictReader(f, delimiter=delimiter)]

    with open(os.path.join(path, "people.csv"), "r", encoding="utf-8") as f:
        people = [Person(r["id"], r["name"], int(r["age"]), r["gender"] == "férfi", r["daycare_id"]) for r in csv.DictReader(f, delimiter=delimiter)]

    with open(os.path.join(path, "pets.csv"), "r", encoding="utf-8") as f:
        pets = [Pet(r["id"], r["name"], r["species"], int(r["age"]), r["owner_id"]) for r in csv.DictReader(f, delimiter=delimiter)]

    return daycares, people, pets

#excel
def write_xlsx(daycares: list[Daycare], people: list[Person], pets: list[Pet], file_path: str) -> None:
    wb = Workbook()
    wb.remove(wb.active)

    #napkozi
    ws_d = wb.create_sheet("daycares")
    ws_d.append(["id", "name", "city", "daily_fee"])
    for d in daycares:
        ws_d.append([d.id, d.name, d.city, d.daily_fee])

    #gazdi
    ws_p = wb.create_sheet("people")
    ws_p.append(["id", "name", "age", "gender", "daycare_id"])
    for p in people:
        ws_p.append([p.id, p.name, p.age, "férfi" if p.male else "nő", p.daycare_id])

    #allat
    ws_pet = wb.create_sheet("pets")
    ws_pet.append(["id", "name", "species", "age", "owner_id"])
    for pet in pets:
        ws_pet.append([pet.id, pet.name, pet.species, pet.age, pet.owner_id])

    wb.save(file_path)

def read_xlsx(file_path: str) -> tuple[list[Daycare], list[Person], list[Pet]]:
    wb = openpyxl.load_workbook(file_path)

    daycares = [
        Daycare(r[0], r[1], r[2], int(r[3]))
        for r in wb["daycares"].iter_rows(min_row=2, values_only=True) if r[0] is not None
    ]
    people = [
        Person(r[0], r[1], int(r[2]), r[3] == "férfi", r[4])
        for r in wb["people"].iter_rows(min_row=2, values_only=True) if r[0] is not None
    ]
    pets = [
        Pet(r[0], r[1], r[2], int(r[3]), r[4])
        for r in wb["pets"].iter_rows(min_row=2, values_only=True) if r[0] is not None
    ]

    return daycares, people, pets