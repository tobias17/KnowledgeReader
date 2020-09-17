import pickle

def save_zones(obj):
    with open('zones.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_zones():
    with open('zones.pkl', 'rb') as f:
        return pickle.load(f)

zone_to_points_rem = load_zones()

x = {k: v for k, v in sorted(zone_to_points_rem.items(), reverse=True, key=lambda item: item[1])}

for zone in x:
    print(f'{zone}: {x[zone]}')