import os
from generator import generate_daycares, generate_people, generate_pets
from handlers import write_json, read_json, write_csv, read_csv, write_xlsx, read_xlsx

def main() -> None:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    #adatok
    daycares = generate_daycares(5, unique=True)
    people = generate_people(30, daycares=daycares)
    pets = generate_pets(45, owners=people)

    print(f"generálás: {len(daycares)} napközi, {len(people)} gazdi, {len(pets)} kisállat\n")

    #json
    write_json(daycares, people, pets, output_dir)
    d_json, p_json, pet_json = read_json(output_dir)
    print(f"json: {len(d_json)} napközi, {len(p_json)} gazdi, {len(pet_json)} kisállat")
    assert d_json == daycares and p_json == people and pet_json == pets

    #csv
    write_csv(daycares, people, pets, output_dir)
    d_csv, p_csv, pet_csv = read_csv(output_dir)
    print(f"csv:  {len(d_csv)} napközi, {len(p_csv)} gazdi, {len(pet_csv)} kisállat")
    assert d_csv == daycares and p_csv == people and pet_csv == pets

    #excel
    xlsx_path = os.path.join(output_dir, "pet_daycare.xlsx")
    write_xlsx(daycares, people, pets, xlsx_path)
    d_xlsx, p_xlsx, pet_xlsx = read_xlsx(xlsx_path)
    print(f"excel: {len(d_xlsx)} napközi, {len(p_xlsx)} gazdi, {len(pet_xlsx)} kisállat")
    assert d_xlsx == daycares and p_xlsx == people and pet_xlsx == pets

if __name__ == "__main__":
    main()