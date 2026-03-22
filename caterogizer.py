from collections import defaultdict
from variants import VARIANTS,FURNITURE_TYPE
#a simple python programme that take the furniture of eco wiki, and reorganize them together grouping by the matial

class furniture():

    def __init__(self,furniture_name):
        self.count=0
        self.before_variant=""
        self.after_variant=""
        self.variant=[]
        self.type="<!--Type-->"
    def to_string(self):
        wiki_name=""
        wiki_group=f"{self.before_variant} {self.after_variant}"
        if not self.variant:
            wiki_name="[["+wiki_group+"]]"
        else:
            for v in self.variant:
                #jump the first <br>
                if v==self.variant[0]:
                    wiki_name+=f"[[{self.before_variant} {v} {self.after_variant}]]"
                    continue
                wiki_name+=f"<br>[[{self.before_variant} {v} {self.after_variant}]]"
        return f"|-\n|{wiki_name}||{wiki_group}||{self.type}||<!--Value-->||<!--Yield-->||<!--volume-->|"

# 🔹 read file
grouped_fourniture={}

with open("furniture.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for line in lines:
    line_name = line.strip()
    if not line_name:
        continue

    words = line_name.split()
    variant_found = None
    furniture_type = ""

    # 🔹 parcourir tous les mots pour trouver la variante et le type
    for i, word in enumerate(words):
        # find variant (only first variant if multiple)
        if word in VARIANTS and variant_found is None:
            variant_found = word
            before = " ".join(words[:i])
            after = " ".join(words[i + 1:])

        # find furniture type
        if word in FURNITURE_TYPE:
            furniture_type = FURNITURE_TYPE[word]

    # si aucune variante trouvée
    if variant_found is None:
        before = line_name
        after = ""

    key = (before, after)  # tuple comme clé

    # 🔹 créer ou récupérer l’objet furniture
    if key not in grouped_fourniture:
        obj = furniture(line_name)
        obj.before_variant = before
        obj.after_variant = after
        obj.type = furniture_type
        grouped_fourniture[key] = obj
    else:
        obj = grouped_fourniture[key]

    # 🔹 ajouter la variante
    if variant_found:
        if variant_found not in obj.variant:
            obj.variant.append(variant_found)

    # 🔹 mettre à jour le count
    obj.count = len(obj.variant)


with open("template_houssingValue.txt", "w", encoding="utf-8") as f:

    f.write("https://github.com/reddrims/eco_wiki ,may requier some manual input\n")
    f.write('{| class="wikitable sortable"\n')
    f.write("!Furniture Variants !! Group Furniture !! Furniture Type !! Housing Value !! Yield !! Volume Required !! Notes\n")
    for obj in grouped_fourniture.values():
        f.write(obj.to_string() + "\n")