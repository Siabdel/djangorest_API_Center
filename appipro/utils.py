
## La digitalisation des commercant locaux,
## commerce de proximite
""
-
www.epicerie.com
Abonnement : 300 euros / mois
commission : 5%
"""
import pandas as pd
import json
from appipro import models
from pandas.io.json import json_normalize


## simple trucks List Comprehensions
# Iterating over one column - `f` is some function that processes your data
result = [f(x) for x in df['col']]
# Iterating over two columns, use `zip`
result = [f(x, y) for x, y in zip(df['col1'], df['col2'])]
# Iterating over multiple columns - same data type
result = [f(row[0], ..., row[n]) for row in df[['col1', ...,'coln']].to_numpy()]
# Iterating over multiple columns - differing data type
result = [f(row[0], ..., row[n]) for row in zip(df['col1'], ..., df['coln'])]


## dict to object.
class Dictate(object):
    """Object view of a dict, updating the passed in dict when values are set
    or deleted. "Dictate" the contents of a dict...: """

    def __init__(self, d):
        # since __setattr__ is overridden, self.__dict = d doesn't work
        object.__setattr__(self, '_Dictate__dict', d)

    # Dictionary-like access / updates
    def __getitem__(self, name):
        value = self.__dict[name]
        if isinstance(value, dict):  # recursively view sub-dicts as objects
            value = Dictate(value)
        return value

    def __setitem__(self, name, value):
        self.__dict[name] = value
    def __delitem__(self, name):
        del self.__dict[name]

    # Object-like access / updates
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value
    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.__dict)
    def __str__(self):
        return str(self.__dict)



# lecture fichier data json
data = json.load(open("appipro/data/data.json"))

#
df = pd.json_normalize(data)

dfr = df['results']

queryset  = dfr.iteritems()

## objects
## python -m pip install 'python-language-server[all]'
cc = models.StaffDirectory.objects.first()

for key, val in  queryset :
    print("key={} val={}".format(key, val))
    ## insert les enregistrements en base
    ##
    cc.create(user_id=1,
        category_id=2,
        title = val.gender,
        nom = val.name.last,
        prenom = val.name.first,
        adresse = val.location.street.number + " " + val.location.street.name ,
        ville = val.location.city,
        codepostal = val.location.postcode,
        pays = val.location.country,
        latitude = val.coordinates.latitude,
        longitude = val.coordinates.longitude,
        email = val.email,
        telephone = val.phone,
        )


##################
## lecture fichier data json
data = json.load(open("appipro/data/data.json"))
df = pd.json_normalize(data)

for i,row in data.iterrows():
    sql = "INSERT INTO `book_details` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
    cursor.execute(sql, tuple(row))


####################

# lecture fichier data json
data = json.load(open("appipro/data/data.json"))

##
df = pd.json_normalize(data)

dfr = df.results.array
##
queryset = dfr.all()

for elem in queryset :
    print(elem['name'])
    cc.create(user_id=1,
        category_id=2,
        title = elem['gender'],
        nom = elem['name.last'],
        prenom = elem['name.first'],
        adresse = elem['location.street.number'] + " " + elem['location.street.name'], ,
        ville = elem['location.city'],
        codepostal = elem['location.postcode'],
        pays = elem['location.country'],
        latitude = elem['coordinates.latitude'],
        longitude = elem['coordinates.longitude'],
        email = elem['email'],
        telephone = elem['phone'],
        )

########################################
import json
from collections import namedtuple

json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

####################################


# lecture fichier data json
data = json.load(open("appipro/data/data.json"))

# passe en data panda
df = pd.json_normalize(data)

##
dfr = df.results.array

data_arr = pd.DataFrame.from_dict(dfr)

cc = models.StaffDirectory.objects.all()
##
for i, elem in data_arr.iterrows() :
    print(elem )
    cc.create(user_id=1,
        category_id=2,
        title = elem.gender,
        nom = elem['name']['last'],
        prenom = elem.name['first'],''
        adresse = elem['location']['street']['number'] + " " + elem['location']['street']['name'] ,
        ville = elem['location']['city'],
        codepostal = elem['location'][.postcode],
        pays = elem['location']['country'],
        latitude = elem['coordinates']['latitude'],
        longitude = elem['coordinates']['longitude'],
        email = elem.email,
        telephone = elem.phone,
        )
#########################

def import_json():
    ## lecture fichier data json
    data = json.load(open("appipro/data/data.json"))

    # passe en data panda
    dd = data['results']
    data_arr = pd.DataFrame(dd)

    cc = models.StaffDirectory.objects
    #
    for elem in data_arr.itertuples() :
     print(elem)
     cc.create(user_id=1,
         category_id=2,
         title = elem.gender,
         nom = elem['name']['last']
         prenom = elem['name']['first'],
         adresse = elem['location']['street']['number'] + " " + elem['location']['street']['name'] ,
         ville = elem['location']['city'],
         codepostal = elem['location']['postcode'],
         pays = elem['location']['country'],
         latitude = elem['coordinates']['latitude'],
         longitude = elem['coordinates']['longitude'],
         email = elem.email,
         telephone = elem.phone,
         )
#########################"

def import_json():
    ## lecture fichier data json
    data = json.load(open("appipro/data/data.json"))

    # passe en data panda
    dd = data['results']

    cc = models.StaffDirectory.objects.all()
    #
    for elem in dd :
     print(elem )
     cc.create(user_id=1,
         category_id=2,
         title = elem['gender'],
         nom = elem['name']['last'],
         prenom = elem['name']['first'],
         adresse = str(elem['location']['street']['number']) + " " + elem['location']['street']['name'] ,
         ville = elem['location']['city'],
         codepostal = elem['location']['postcode'],
         pays = elem['location']['country'],
         latitude = elem['location']['coordinates']['latitude'],
         longitude = elem['location']['coordinates']['longitude'],
         email = elem['email'],
         telephone = elem['phone'],
         )
