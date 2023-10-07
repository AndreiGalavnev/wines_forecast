# для выпадающего меню для выбора на странице
def lists_for_streamlit(path):
    countries_list = []
    regions_list = []
    types_list = ['Fortified Wine', 'Dessert wine', 'Sparkling wine']
    grapes_list = []

    with open(f'{path}', 'r', encoding='utf-8') as f:
        s = f.readlines()
        # reading countries
        for i in s[2::10]:
            countries_list.append(i[10:-2])
        countries_list = list(set(countries_list))
        # reading regions (for fortified, sparkling and dessert)
        for i in range(len(s)):
            if i % 10 != 3:
                continue
            else:
                if s[i+2] in ['Wine type - Fortified Wine.\n', 'Wine type - Dessert wine.\n', 'Wine type - Sparkling wine.\n']:
                    r = s[i]
                    regions_list.append(r[9:-2])
        regions_list = list(set(regions_list))
        # reading grapes
        for i in s[6::10]:
            grapes_list.append(i[16:-2])
        grapes_list = list(set(grapes_list))
        return countries_list, regions_list, types_list, grapes_list
