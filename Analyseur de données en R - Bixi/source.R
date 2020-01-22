### Pascal Pelletier-Thériault

###importStations
###
###
## Fonction important les données fournies des stations par Bixi selon le fichier voulu
##
## Argument
##
## file : Chemin vers le fichiers csv de Bixi des stations incluant le nom du fichier ou le nom du fichier s'il est dans le même répertoire que "source.R".
##
## Valeur
##
## Tableau des données fournies par Bixi où la première colonne correspond aux codes des stations
## et la deuxième à leur nom en texte.
##
## Exemple
##
## importStations("data/Stations_2018.csv")
##

importStations <- function(file) {
  
  read.csv(
    file,
    colClasses = c(code = "integer",
                   name = "character"),
    encoding = "UTF-8")[1:2] # Ne garde que les colonnes 1 et 2 dont le type d'importation a été spécifié
}


###importData
###
###
## Fonction important les données d'utilisation fournies par Bixi selon l'intervalle donné de temps
##
## Arguments
##
## start : première date dans le format texte suivant a-m-j (y-m-d)
## end : deuxième date dans le format texte suivant a-m-j (y-m-d)
## (Les dates fournies ne peuvent contenir un ou des mois absents du répertoire)
## path : Chemin vers le répertoire contenant les fichiers csv de Bixi
##
## Valeur
##
## Tableau des données fournies par Bixi où les dates sont dans l'intervalle donnée
##
## Exemple
##
## importData("2018-07-01","2018-09-09","data")
##

importData <- function(start, end, path = "") {
  
  Chemin = Path(start, end, path)
  
  x <- NULL #initialisation de x qui sera le Dataframe des données
  for (i in 1:length(Chemin)) {
    x <- rbind(x,
               read.csv(
                 file = Chemin[i],
                 colClasses = c(
                   start_date = "Date",
                   start_station_code = "factor",
                   end_date = "Date",
                   end_station_code = "factor",
                   duration_sec = "numeric",
                   is_member = "factor"
                 ),
                 encoding = "UTF-8" # Encodage des csv
               ))
  }
  subset(x, start_date >= as.Date(start) &
           start_date <= as.Date(end)) # Filtre le tableau crée
}


###Path
###
###
## Fonction créant un vecteur des chemins nécessaires pour importData
##
## Arguments
##
## start : première date dans le format texte suivant a-m-j (y-m-d)
## end : deuxième date dans le format texte suivant a-m-j (y-m-d)
## path : Chemin vers le répertoire contenant les fichiers csv de Bixi
##
## Valeur
##
## Vecteur contenant les différents chemins vers les différents fichiers
##
## Exemple
##
## Path("2018-07-01","2018-09-09","data")
##

Path <- function(start, end, path) {
  
  start = as.Date(start)
  end = as.Date(end)
  
  Annee_Mois <-
    format(seq.Date(start, end, by = 28), "%Y-%m") #Crée un vecteur de forme "année-mois" (ex : "2018-05")
  
  #seq.Date compte seulement par mois complet avec «by ="month"» doit, donc être inférieur à la durée minimal d'un mois pour que toute les mois autres
  # que le dernier sois « toujours » inclus.
  
  Annee_Mois <-
    unique(c(Annee_Mois, format(as.Date(end), "%Y-%m"))) # Ajoute le dernier mois, dans les cas de type 2018-05-31, 2018-06-01 qui sont omis
  # par seq. Unique s'assure que chaque mois n'est présent qu'une fois.
  
  if (path == ""){ 
    paste0("OD_", Annee_Mois, ".csv") # Vecteur contenant les différents chemins vers les différents fichiers ()
  }
  else{
    file.path(path, paste0("OD_", Annee_Mois, ".csv")) # Vecteur contenant les différents chemins vers les différents fichiers
  }
}


###getStations
###
###
## Fonction extractant d'un tableau donné les codes des stations
##
## Arguments
##
## data : un tableau dont la première colonne est remplie des codes correspondants des stations
##        en format nombre et une deuxième colonne contenant le nom des stations en format texte.
## name : un vecteur de mots/noms correspondant aux stations recherchées.
##
## Valeur
##
## Liste nommée de vecteur des codes de stations pour le ou les noms données.
##
## Exemple
##
## getStations(importStations("data/Stations_2018.csv"),"Rachel")
##
getStations <- function(data, name) {
  
  mapply(function(name) {
    #Pour le premier élément de name cherche s'il y a une correspondance dans la colonne "name"
    data[grep(name, data$name), 1] #du tableau, puis refait pour le deuxième élément, etc; et retourne une liste de vecteur nommé.
    
  }, name, SIMPLIFY = FALSE, USE.NAMES = TRUE)
}


###summary.duration
###
###
## Fonction appliquant la fonction summary aux durées des locations du tableau fournie par l'utilisateur.
## La fonction summary donne des informations comme la médiane, moyenne, minimum, maximum, etc.
##
## Arguments
##
## x : un tableau dont le format est celui d'un tableau crée par Importdata.
## per.status : peut avoir comme valeur TRUE ou False, cela détermine l'inclusion ou la séparation des membres/non-membres
##
## Valeur
##
## Liste nommée si per.status est vrai des données de durée de location fournies
## calculées par summary pour les non-membres et les membres séparés, sinon
## simplement la fonction summary sur toutes les données de durée de location du
## tableau donné.
##
## Exemples
##
## summary.duration(importData("2018-04-01","2018-04-30","data"),TRUE)
## summary.duration(importData("2018-04-01","2018-04-30","data"),FALSE)
##

summary.duration <- function(x, per.status = FALSE) {
  
  ifelse(per.status == TRUE,
         
         return(list(                                    # Les listes ne sont pas retournées complètes et nommées sans un return
           "0" = summary(x$duration_sec[x$is_member == 0]),
           "1" = summary(x$duration_sec[x$is_member == 1]))), 
         return(summary(x$duration_sec)))
}


###summary.rentals
###
###
## Fonction calculant le nombre total d'emprunt, le nombre total de location faite par les membre et
## la fraction de location faite par les non-membres sur le total d'emprunt.
##
## Arguments
##
## x : un tableau dont le format est celui d'un tableau crée par Importdata.
##
## Valeur
##
## Vecteur de longueur 3 dont la première valeur est la quantité totale de location du tableau fourni,
## la deuxième le nombre de location faite par les membre et la troisième la fraction de location faite par
## les non-membres sur le total d'emprunt
##
## Exemple
##
## summary.rentals(importData("2018-04-01","2018-04-30","data"))
##

summary.rentals <- function(x) {
  
  c(t <-length(x$start_date),
    m <- length(x[x$is_member == 1, 6]), # x est filtré pour ne garder que les lignes où l'emprunt a été fait par
    p <- m / t)                          # un membre, puis transformé en vecteur avec les données de la colonne 6,
  # puis compté.
}


###revenues
###
###
## Fonction calculant le coût de la location en fonction du temps(x) en secondes et qui retourne cette somme.
## Le prix est établi selon une fonction donné (FUN)).
##
## Arguments
##
## x : temps en secondes
## Fun : Une fonction permettant d'obtenir le coût de location pour une durée donnée
##
## Valeur
##
## Somme de tous les prix chargés pour la durée des locations donnés.
##
## Exemple
##
## revenues(data.frame(start_date = as.Date("2018-05-09"),start_station_code = as.factor(c(6226, 6214)),end_date = as.Date("2018-05-09"),end_station_code = as.factor(c(6033, 6181)), duration_sec = c(904, 404), is_member = as.factor(c(1, 1))),sum)
## 

revenues <- function(x, FUN) {
  
  sum(FUN(x$duration_sec))
}


###tariff_A2019r1
###
###
## Fonction calculant le coût de la location en fonction du temps(x) en secondes et qui retourne cette somme.
## Le prix est établi selon des bornes de temps (moins de 1800 secondes = 2.95$, entre 1800 et 2700 secondes = 4.75$, etc.).
##
## Argument
##
## x : temps en secondes
##
## Valeur
##
## Coût pour le temps donné
##
## Exemples
##
## tariff_A2019r1(0)
## tariff_A2019r1(1861)
##

tariff_A2019r1 <- function(x) {
  
  ifelse(1800 <= x &
           x <= 2700, 4.75, ifelse(2700 < x, (as.integer((
             x - 2701
           ) / 900) + 1) * 3 + 4.75, 2.95)) # Test dans quelles bornes est x et applique la facturation appropriée.
  # (Pour x supérieurs à 2700: retire 2701 et divise
  # par 900 pour trouver le nombre de tranches de 900
  # secondes (15 minutes) supplémentaires. Arrondie le
  # le nombre à l'entier inférieur et y ajoute 1 pour la
  # première tranche non comptée. Puis, multiplie par 3
  # pour obtenir le coût de ces tranches et les ajouts
  # au coût des 2700 premières secondes.)
}


###tariff_A2019r2
###
###
##
## Fonction calculant le coût de la location en fonction du temps(x) en secondes et qui retourne cette somme.
## Le prix est établi selon des bornes de temps (moins de 1800 secondes = 0.00109$/secondes + coût de base, entre 1800 et 2700
## secondes = prix pour 1799 secondes + 0.00299$/secondes pour les secondes dépassant 1799, etc; avec un maximum de 10.50$)
##
## Argument
##
## x : temps en secondes
##
## Valeur
##
## Coût pour le temps donné
##
## Exemples
## tariff_A2019r2(0)
## tariff_A2019r2(1861)
## 

tariff_A2019r2 <- function(x) {
  
  x <- ifelse(x < 0, 0, x)
  ifelse(x <= 1800, x * 0.00109 + 0.57, ifelse((
    "tarif" <-
      0.00299 * (x - 1800) + 1800 * 0.00109 + 0.57
  ) < 10.5, tarif, 10.5)) # Test le type de facturation à faire et les appliques selon le cas.
  # (moins de 1800 secondes: nb de secondes * Coût par secondes + coût de base)
  # Plus de 1800 secondes: La plus petit valeur entre le maximum pouvant
  # être chargé et le nb de secondes * le coût par secondes + le coût pour
  # les 1800 premières secondes + le coût de base.
}