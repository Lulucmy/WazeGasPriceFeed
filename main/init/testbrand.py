from config import Init

#  Calculating similarity between brands (to avoid matching different brands)
## Only used for testing
def matchbrands(brand1, brand2, name1, name2):
    brand1, brand2, name1, name2 = map(str.lower, [brand1, brand2, name1, name2])

    brand1_match = None
    brand2_match = None
    match = False
    
    for brand_list_name, brands in Init.__brandnames__.items():
        brand1_words = brand1.split()
        name1_words = name1.split()
        station1 = brand1_words + name1_words
        brand2_words = brand2.split()
        name2_words = name2.split()
        station2 = brand2_words + name2_words

        for i in station1:
            if i in brands:
                brand1_match = brand_list_name
                break
        for i in station2:
            if i in brands:
                brand2_match = brand_list_name
                break
        if (brand1_match == brand2_match) & (brand1_match != None) & (brand2_match != None):
            print(f"matchbrands: {brand1_match} {brand2_match}")
            match = True
            break
            
    return match

print(matchbrands("super u", "systeme u", "relais de la liberte", "u"))