Noun = {
  'all': set("K Q R M O T V S C X D N W U L Z P j d s l f e i m z o w".split()),
  'number__Plur': set('T K'.split()),
  'number__Sing': set('M R P Q K O'.split()),
  'gender_Masc': set('T M R P Q O K'.split()),
  'gender_Fem':  set('T M R P K'.split()),
  'gender_Neut': set('U T M R P K'.split()),
  'case_Nom': set('Q O K'.split()),  # mianownik
  'case_Gen': set('T M R P Q O K'.split()),  # dopełniacz
  'case_Dat': set('M Q O K'.split()),  # celownik
  'case_Acc': set('M Q O K'.split()),  # biernik
  'case_Ins': set('M Q O K'.split()),  # narzednik
  'case_Loc': set('Q O K'.split()),  # miejscownik
  'case_Voc': set('M Q O'.split()),  # wołacz
}