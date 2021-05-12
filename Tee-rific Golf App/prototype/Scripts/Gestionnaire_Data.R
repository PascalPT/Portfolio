#### tp: Pascal, Geneviève, Charles, Michaël
###
### Data_Tro
###
## Fonction trouvant les erreurs dans des données.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## complètes : Une valeur booléenne indiquant si data contient les données
##            complètes/initales des modèles.
##
## Valeur
##
## Un tableau de données des trous joués pour chaque quatuor où les erreurs à
## corriger sont marqué par des Inf.
##
## Exemple
##
## Data_Tro(data, complètes)
##
Data_Tro <- function(data, complètes = TRUE) {
  ## Flag/drapeau pour signifier que les paramètres doivent être recalculés.
  ## (Les réinitialisent)
  if (complètes) {
    Norm_Norm_para <- c(sigma = 0,
                        sigma_0 = 0,
                        mu_0 = 0)

    Bin_Bet_PAR_para <- c(
      a_3 = 0,
      b_3 = 0,
      n_3 = 0,
      a_4 = 0,
      b_4 = 0,
      n_4 = 0,
      a_5 = 0,
      b_5 = 0,
      n_5 = 0
    )

    Bin_Bet_NOR_para <- c(a_norm = 0 ,
                          b_norm = 0,
                          n_norm = 0)

    Poi_Gam_NOR_para <- c(lamda_P = 0, alpha_P = 0)

    Bulh_para <- c(m = 0, K = 0)

    Bulh_Str_para <- c(m_s = 0, K_s = 0)

    assign("Norm_Norm_para", Norm_Norm_para , envir = .GlobalEnv)
    assign("Bin_Bet_PAR_para", Bin_Bet_PAR_para , envir = .GlobalEnv)
    assign("Bin_Bet_NOR_para", Bin_Bet_NOR_para , envir = .GlobalEnv)
    assign("Poi_Gam_NOR_para", Poi_Gam_NOR_para , envir = .GlobalEnv)

    assign("Bulh_para", Bulh_para , envir = .GlobalEnv)

    assign("Bulh_Str_para", Bulh_Str_para , envir = .GlobalEnv)
  }

  data[data < 1] <- -Inf

  # Remplace les Na par des Inf si les données sont complètes, car Inf est la
  # valeurs qui marque une donnée à corriger pour Data_Cor(...).
  if (complètes) {
    data[is.na(data)] <- -Inf
  }

  ## Les valeurs négatives ou trop grosse sont marqué pour la correction.
  data_temp <- data[, -1]
  data_temp[data_temp > 15] <- -Inf
  data[, -1] <- data_temp
  data
}
###
###
### Data_Cor
###
## Fonction corrigeant les erreurs marqués par Inf dans des données.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor avec des
##        erreurs marqués à la correction.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## m_multiple : pourcentage de données manquantes acceptée.
##
## Valeur
##
## Un tableau de données des trous joués pour chaque quatuor où les erreurs à
## corriger ont été remplacées par la moyenne arrondis du quatuor sans les
## données trop corrompus.
##
## Exemple
##
## Data_Cor(data, normales_data, m_multiple)
##
Data_Cor <- function(data,
                     normales_data = read.csv2("Data/normales.csv"),
                     m_multiple = 0.15) {
  # Transformer m_multiple en nombre de trous.
  m_multiple <- round(m_multiple * length(normales_data))

  # Créer une nouvelle colonne des résultats totaux.
  data$Résultat_ronde <-
    rowSums(data[, 2:(length(normales_data) + 1)], na.rm = TRUE)

  # Crée un index des lignes ayant des problèmes (dont le résultat est négatif).
  index <- data[data$Résultat_ronde <= 0, 1]

  # vecteur contenant l'index des lignes trop corrompus.
  Cor_data <- c()

  for (i in index) {
    # trouve toutes les données marquées pour correction dans la ligne i.
    x <-
      unlist(as.list(data[i, 2:(length(normales_data) + 1)] == -Inf,
                     use.names = FALSE))
    # Retire les NA des données à corriger.
    x[is.na(x)] <- FALSE

    # Calcule le ratio moyen par rapport à la normale pour le quatuor i.
    y <-
      (sum(data[i, 2:(length(normales_data) + 1)][!x] /
             unlist(normales_data[!x], use.names = FALSE), na.rm = TRUE) /
         (length(normales_data) - length(x[x == TRUE])))
    # Remplace les données marquées à corriger par le ratio multiplié par la
    # normale des trous à corriger arrondi.
    data[i, 2:(length(normales_data) + 1)][x] <-
      round(normales_data[1, ] * y)[x]

    # Marque la ligne à supprimer s'il y a trop de données manquantes.
    if (length(x[x == TRUE]) > m_multiple) {
      Cor_data <- append(Cor_data, i)
    }
  }

  if (length(Cor_data) != 0) {
    # Retourne les données corrigées sans les observations trop corrompus.
    data[-1 * Cor_data, ][1:(length(normales_data) + 1)]
  }
  else{
    # Sinon retourne toutes les données corrigées.
    data[1:(length(normales_data) + 1)]
  }
}
###
###
### Data_Norm
###
## Fonction calculant le ratio par rapport à la normale pour chaque trou.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## Valeur
##
## Un tableau de données des trous joués pour chaque quatuor où les résultats
## pour chaque trou est le ratio par rapport à la normale du trou. Une colonne
## du résultats totaux normalisés est aussi ajoutée.
##
## Exemple
##
## Data_Norm(data, normales_data)
##
Data_Norm <- function(data,
                      normales_data = read.csv2("Data/normales.csv")) {
  # Calcul le ratio par rapport la normale pour chaque trou des quatuors.
  data[2:(length(normales_data) + 1)] <-
    (data[2:(length(normales_data) + 1)] /
       normales_data[col(data)])

  # Calcul le ratio de la normale du résultat de la ronde des quatuors.
  data$Résultat_ronde_normalisé         <-
    rowMeans(data[2:(length(normales_data) + 1)], na.rm = TRUE)
  data
}
###
###
### Data_Incom
###
## Fonction créant des données trouées à partir de données complètes.
##
## Arguments
##
## data : un tableau complèt de données des trous joués pour chaque quatuor.
##
## m_multiple : Le pourcentage de trous à garder, qui sera considérés joués.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## len : pourcentage des quatuors à sélectionner, qui seront gardés.
##
## seed : Valeur numérique du point de départ d'un algorithme pseudo-aléatoire.
##
## Valeur
##
## Un tableau de données des trous joués pour les quatuors sélectionnés dont une
## certaines quantités des trous joués est marqués comme manquants par des NA.
##
## Exemple
##
## Data_Incom(data, m_multiple, len, seed)
##
Data_Incom <- function(data,
                       m_multiple = 1 / 3,
                       normales_data = read.csv2("Data/normales.csv"),
                       len = 0.25,
                       seed = 1) {
  # Mettre m_multiple en nombres de trous.
  m_multiple <- round(m_multiple * length(normales_data))

  # Format des données => trouver le nombre de lignes/colonnes totals.
  nb_row <- length(data[, 1])
  nb_holes <- length(normales_data)
  col_holes <- nb_holes + 1

  # Mise en place du point de départ de l'algorithme pseudo-aléatoire de R.
  set.seed(seed = seed)

  # Sélection des quatuors à garder.
  data_lin <-
    sort(sample(data$Game_ID, round(len * nb_row)))

  # Sélection du premier trous joués par les quatuors sélectionnés.
  # (runif discrète {0 à 17, donc + 1} à partir de runif)
  data_col <- floor(runif(round(len * nb_row)) * nb_holes) + 1

  # Création de la liste de vecteurs des trous joués pour les quatuors.
  # sélectionnés.
  data_col <- lapply(data_col, function(x) {
    x:(x + m_multiple - 1)
  })
  # Format des vecteur des trous joués pour les quatuors sélectionnés. Les trous
  # supérieur aux nombres de trous sont ramener/enrouler à 1,2,3...
  # (wrap around) => ex: c(18,19,20) devient c(18,1,2).
  data_col <- lapply(data_col, function(x) {
    x[x > nb_holes] <- x[x > nb_holes] - nb_holes
    x
  })

  # Création du tableau ayant des données trouées et seulement certains
  # quatuors. Une colonne des résultats réels des rondes est ajouté pour pouvoir
  # voir la précision des modèles.
  data_incom <- data[data_lin, ]
  data_incom$résultats_réels <-
    rowSums(data_incom[2:col_holes], na.rm = TRUE)

  # Suppression des données non-selectionnées
  for (i in 1:length(data_col)) {
    data_incom[2:col_holes][i, -unlist(data_col[i])] <- NA
  }

  data_incom

}