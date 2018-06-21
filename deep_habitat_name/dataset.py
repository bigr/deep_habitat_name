import requests
import os

def get_habitat_names(country, cache=True):

    cache_file = country+'-names.cache'

    if cache and os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            data = f.read()
        return [v.decode().lower() for v in data.splitlines()][1:]


    #url = 'http://overpass-api.de/api/interpreter'
    url = 'https://overpass.openstreetmap.fr/api/interpreter'
    #url = 'http://overpass.osm.ch/api/interpreter'
    #url = 'http://overpass.openstreetmap.ru/cgi/interpreter'
    #url = 'https://overpass.kumi.systems/api/interpreter'

    query = """
        [out:csv (name)];
        
        rel
          ["boundary"="administrative"]  
          ["admin_level"="2"]
          ["ISO3166-1"="{}"];
        
        
        map_to_area;
        
        (node
          ["place"~"city|town|village|hamlet"]
          (area);
        );
        out body qt;
    """.format(country)

    response = requests.post(url,{'data':query})

    with open(cache_file,'wb') as f:
        f.write(response.content)

    return [v.decode().lower() for v in response.content.splitlines()][1:]