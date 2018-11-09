"""
Generates shareholders for testing purposes
"""

import random, os
from app import db
from app.models import Status, Company, Individual

if os.environ.get('OSAYHING_DEBUG') is None:
    OSAYHING_DEBUG = True

m = ["Martin", "Markus", "Nikita", "Romet", "Oliver", "Oskar", "Sander", 
    "Robert", "Kristofer", "Kaspar", "Sebastian", "Daniel", "Artur", "Marten", 
    "Mattias", "Kevin", "Aleksandr", "Hänk", "Amor", "Printz", "Stiiv", "Leek", 
    "Riff", "Tõru", "Rivendell", "Vesse", "Vakk", "Ozzy", "Vitalik", "Kaius", 
    "Karm", "Karla", "Kregor Morris", "Pent Ramses", "Theodor", "Cornelius", 
    "Nils Niklas", "Thor Meri", "Roel", "Aiden", "Sander", "Aleksander", 
    "Kristjan", "Kevin", "Nikita", "Markus", "Artur", "Maksim", "Karl", 
    "Dmitri", "Daniil", "Siim", "Rasmus", "Aleksei", "Andrei", "Artjom", 
    "Ilja", "Mihkel"]
f = ["Sandra", "Milana", "Lisandra", "Anna", "Viktoria", "Emma", "Mirtel", 
    "Mia", "Liisa", "Polina", "Marta", "Alisa", "Arina", "Diana", "Hanna",
    "Eliise", "Emilia", "Sohvi", "Säde", "Kleopatra", "Sume", "Tuule", 
    "Kirsi Mari", "Pihla Mari", "Susi", "Suvi", "Sireli", "Suzet Meribel",
    "Rosiine", "Karoliine", "Mathilda Juuli", "Säsili", "Pipi", "Linda", 
    "Päike", "Sära", "Marii Loreen", "Siidi Loore", "Rilleriin", "Pääsu Lee", 
    "Mann", "Lumi", "Abigail Käbi", "Täheke", "Ella Maria", "Wilhelmina Anna",
    "Laura", "Kristina", "Maria", "Diana", "Sandra", "Anastassia", 
    "Jekaterina", "Karina ", "Alina", "Kristiina", "Aleksandra", "Viktoria",
    "Darja", "Liis", "Kätlin", "Julia", "Valeria", "Triin"]
sn = ["Ivanov", "Tamm", "Saar", "Sepp", "Mägi", "Smirnov", "Vasiliev", 
    "Petrov", "Kask", "Kukk", "Kuznetsov", "Rebane", "Ilves", "Mihhailov", 
    "Pärn", "Pavlov", "Semenov", "Koppel", "Andreev", "Alekseev", "Lepik", 
    "Oja", "Raudsepp", "Kuusk", "Karu", "Fjodorov", "Kütt", "Põder", "Vaher", 
    "Popov", "Stepanov", "Lepp"]
    
    
def generate_dataset(count): 
    dataset = []
    identifications = []   
    birth_id = random.sample(range(1, 5000), count)
    for i, person in enumerate(range(count)):
        if i%2 == 0:
            first_name = m[random.randint(-1, len(m)-1)]
            g=3
        else:
            first_name = f[random.randint(-1, len(f)-1)]
            g=4
        if OSAYHING_DEBUG:
            print(first_name, end=';')        
        surname = sn[random.randint(-1, len(sn)-1)]
        if OSAYHING_DEBUG:
            print(surname, end=';')      
        year =  random.randint(40, 99)
        if OSAYHING_DEBUG:
            print(year, end=';')      
        month = random.randint(1,12)
        if OSAYHING_DEBUG:
            print(month, end=';')      
        if month in [1,3,5,7,8,10,12]:
            day =  random.randint(1,31)
        if month in [4,6,9,11]:
            day =  random.randint(1,30)
        if month == 2:
            day =  random.randint(1,28) # never mind leap year
        if OSAYHING_DEBUG:
            print(day, end=';')
        id = int(g*10e9+year*10e7+month*10e5+day*10e3+birth_id.pop())
        if OSAYHING_DEBUG:
            print(id)
        identifications.insert(id, -1)           
        dataset.append({
            'first_name': first_name, 
            'last_name':surname,
            'identificator':id})
    return dataset
    
def add_individuals(data): 
    dataset = []
    for i, ind in enumerate(data):
        ind_to_add = Individual(
                        first_name=ind['first_name'],   
                        last_name=ind['last_name'],                              
                        identificator=ind['identificator'])
        dataset.append(ind_to_add)
    db.session.bulk_save_objects(dataset)
    db.session.commit()
    return
    
if __name__=="__main__":
    try:
        dataset = []
        qty = int(input("Input dataset size [10...1000] "))
        if qty in range (10,1001):
            dataset = generate_dataset(qty) 
            add_individuals(dataset)
        else:
            print("Quantity between 10 and 1000")
    except Exception as e:
        print("Exception occured\n{0}".format(e,))

