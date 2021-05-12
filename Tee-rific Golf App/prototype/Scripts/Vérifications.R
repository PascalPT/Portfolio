#### tp: Pascal, Geneviève, Charles, Michaël
###
### Vérif_complèts
###
## Fonction vérifiant si les prédictions sur les données complètes sont celles
## attendues
##
## Arguments
##
## complets_data : un tableau de données des trous joués pour chaque quatuor qui
##                 sert d'oberservations initales.
##
## normales_data : un tableau de données des normales pour les trous joués.
##
## Valeur
##
## Un message d'erreur sera imprimé s'il y a lieux.
##
## Exemple
##
## Vérif_complèts(complets_data, normales_data)
##
Vérif_complèts <- function(complets_data =
                   Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv"))),
                           normales_data = read.csv2("Data/normales.csv")) {
  esp_normales_data <- normales_data
  esp_normales_data[1:length(normales_data)] <-
    colMeans(complets_data[2:(length(normales_data) + 1)])

  ### Paramètres
  ################
  ### En testant les normales vs l'espérance des trous certains modèles ont
  ### montré que cela peut améliorer la précision ou la diminuer. Donc, les
  ### modèles où cela s'applique utilisent l'espérance.

  bayes_paramètres(complets_data ,
                   normales_data ,
                   model_B = c("Bin_Bet_PAR"))

  bayes_paramètres(
    complets_data ,
    esp_normales_data,
    model_B = c("Norm_Norm",
                "Bin_Bet_NOR",
                "Poi_Gam_NOR")
  )

  Bühlmann_paramètres(complets_data, esp_normales_data)

  Bühlmann_Straub_paramètres(complets_data, esp_normales_data)
  ################

  ### Prédictions complètes
  ################
  x <- unname(rowSums(
    bayes_modèles(
      complets_data,
      model_B = c("Norm_Norm"),
      normales_data = esp_normales_data
    )
  ))

  y <-
    unname(rowSums(
      bayes_modèles(
        complets_data,
        model_B = c("Bin_Bet_PAR"),
        normales_data = normales_data
      )
    ))

  z <- unname(rowSums(
    bayes_modèles(
      complets_data,
      model_B = c("Bin_Bet_NOR"),
      normales_data = esp_normales_data
    )
  ))

  c <- unname(rowSums(
    bayes_modèles(
      complets_data,
      model_B = c("Poi_Gam_NOR"),
      normales_data = esp_normales_data
    )
  ))


  t <-
    unname(rowSums(
      Bühlmann_modèles(complets_data, normales_data = esp_normales_data)
    ))
  #g <-
  #  unname(rowSums(Bühlmann_modèles(complets_data,
  #             normales_data = esp_normales_data,
  #                   mode = "Iter")))

  f <-
    unname(rowSums(
      Bühlmann_Straub_modèles(complets_data, normales_data = esp_normales_data)
    ))
  ################
  complèts_Résultats <-
    unname(rowSums(complets_data[2:(length(normales_data) + 1)]))

  complèts_Résultats <-  c(
    Norm_Norm = all(complèts_Résultats == x),
    Bin_Bet_PAR = all(complèts_Résultats == y),
    Bin_Bet_NOR = all(complèts_Résultats == z),
    Poi_Gam_NOR = all(complèts_Résultats == c),

    Bulh_Mean = all(complèts_Résultats == t),
    #Bulh_Iter = all(complèts_Résultats == g),

    Bulh_Str_para = (complèts_Résultats == f)
  )

  if (any(!complèts_Résultats)) {
    print(
      paste(
        "Il y a des modèles qui redonnent une prédiction pour un trou",
        "de plus. (Une prédiction sur les données complètes ne redonne pas la",
        "somme, attendus.)"
      )
    )

    stop(paste(
      "Modèle(s) problématique(s) :",
      paste(names(complèts_Résultats[!complèts_Résultats]),
            collapse = ', ')
    ))

  }
}
###
###
### Vérif_Err
###
## Fonction calculant l'écart absolu moyen de tous les modèles aux résultats
## réels.
##
## Arguments
##
## complets_data : un tableau de données des trous joués pour chaque quatuor qui
##                 sert d'oberservations initales.
##
## normales_data : un tableau de données des normales pour les trous joués
##
## m_multiple : Le pourcentage de trous à garder, qui sera considérés joués.
##
## Valeur
##
## Un vecteur ordonné des meilleurs modèles selon l'écart absolu moyen par
## rapport aux résultats réels. Un tableau avec ces données est aussi assigné
## dans l'environement global.
##
## Exemple
##
## Vérif_Err(complets_data, normales_data)
##
Vérif_Err <- function(complets_data =
                  Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv"))),
                      normales_data = read.csv2("Data/normales.csv"),
                      m_multiple = 1 / 3) {
  esp_normales_data <- normales_data
  esp_normales_data[1:length(normales_data)] <-
    colMeans(complets_data[2:(length(normales_data) + 1)])

  data <-
    Data_Incom(complets_data, len = 0.25, m_multiple = m_multiple)
  complets_data_tronq = complets_data[-data$Game_ID,]

  # juste paramètre
  {
    ### En testant les normales vs l'espérance des trous certains modèles ont
    ### montré que cela peut améliorer la précision ou la diminuer. Donc, les
    ### modèles où cela s'applique utilisent l'espérance.

    bayes_paramètres(complets_data_tronq ,
                     normales_data ,
                     model_B = c("Bin_Bet_PAR"))

    bayes_paramètres(
      complets_data_tronq ,
      esp_normales_data,
      model_B = c("Norm_Norm",
                  "Bin_Bet_NOR",
                  "Poi_Gam_NOR")
    )

    Bühlmann_paramètres(complets_data_tronq, esp_normales_data)

    Bühlmann_Straub_paramètres(complets_data_tronq, esp_normales_data)
  }

  # juste prédiction
  {
    x <-
      unname(rowSums(
        bayes_modèles(
          data[1:(length(normales_data) + 1)],
          model_B = c("Norm_Norm"),
          normales_data = esp_normales_data
        )
      ))
    y <-
      unname(rowSums(bayes_modèles(data[1:(length(normales_data) + 1)],
                                   model_B = c("Bin_Bet_PAR"))))
    z <-
      unname(rowSums(
        bayes_modèles(
          data[1:(length(normales_data) + 1)],
          model_B = c("Bin_Bet_NOR"),
          normales_data = esp_normales_data
        )
      ))
    c <-
      unname(rowSums(
        bayes_modèles(
          data[1:(length(normales_data) + 1)],
          model_B = c("Poi_Gam_NOR"),
          normales_data = esp_normales_data
        )
      ))

    g <-
      unname(rowSums(
        Bühlmann_modèles(data[1:(length(normales_data) + 1)],
                         normales_data = esp_normales_data)
      ))
    #t <-
    #  unname(rowSums(Bühlmann_modèles(data[1:(length(normales_data) + 1)],
    #                   normales_data = esp_normales_data,
    #                   mode = "Iter")))

    f <-
      unname(rowSums(
        Bühlmann_Straub_modèles(data[1:(length(normales_data) + 1)],
                                normales_data = esp_normales_data)
      ))
  }

  # bayes err. préd.
  {
    x <- abs(data$résultats_réels - x)
    x <- mean(x)

    y <- abs(data$résultats_réels - y)
    y <- mean(y)

    z <- abs(data$résultats_réels - z)
    z <- mean(z)

    c <- abs(data$résultats_réels - c)
    c <- mean(c)

    Err_préd_bayes <-
      c(
        Norm_Norm = x,
        Bin_Bet_PAR = y,
        Bin_Bet_NOR = z,
        Poi_Gam_NOR = c
      )
  }

  #bulh err. préd.
  {
    g <- abs(data$résultats_réels - g)
    g <- mean(g)

    #t <- abs(data$résultats_réels - t)
    #t <- mean(t)

    Err_préd_bulh <- c(Bulh_Mean = g) #, Bulh_Iter = t)
  }

  #bulh_str err. préd.
  {
    f <- abs(data$résultats_réels - f)
    f <- mean(f)
    Err_préd_bulh_str = c(Bulh_str = f)
  }

  Err_préd = append(Err_préd_bayes, Err_préd_bulh)
  Err_préd = append(Err_préd, Err_préd_bulh_str)


  Err_préd_glob <- as.data.frame(matrix(Err_préd,
                                        nrow = 1,
                                        dimnames = list(c(1),
                                                        names(Err_préd))))

  # juste paramètre pour les remettres dans leurs états initials
  {
    ### En testant les normales vs l'espérance des trous certains modèles ont
    ### montré que cela peut améliorer la précision ou la diminuer. Donc, les
    ### modèles où cela s'applique utilisent l'espérance.

    bayes_paramètres(complets_data_tronq ,
                     normales_data ,
                     model_B = c("Bin_Bet_PAR"))

    bayes_paramètres(
      complets_data_tronq ,
      esp_normales_data,
      model_B = c("Norm_Norm",
                  "Bin_Bet_NOR",
                  "Poi_Gam_NOR")
    )

    Bühlmann_paramètres(complets_data_tronq, esp_normales_data)

    Bühlmann_Straub_paramètres(complets_data_tronq, esp_normales_data)
  }

  assign("Err_préd", round(Err_préd_glob, 2), envir = .GlobalEnv)
  sort(Err_préd)
}
###
###
### Vérif_Norm
###
## Fonction vérifiant les données normales.
##
## Arguments
##
## normales_data : un tableau de données des normales pour les trous joués
##
## Valeur
##
## Un vecteur "booléen" indiquant s'il y a erreur ou non.
## (Il y a aussi un message indiquant s'il y a une erreur et le type d'erreur)
##
## Exemple
##
## Vérif_Norm(normales_data)
##
Vérif_Norm <-
  function(normales_data = read.csv2("Data/normales.csv")) {
    if (NA %in% normales_data) {
      stop(
        paste(
          "Les données des normales comportent une/des erreur(s)/",
          "valeur(s) manquante(s)"
        )
      )
    }
    if (1 %in% normales_data) {
      warning(
        paste(
          "Les données des normales comportent au moins un «Par» 1.",
          "Le modèle Normale-Normale sera donc invalide"
        )
      )
    }
  }
###
###
### Vérif_Data
###
## Fonction vérifiant des données partielles fournies.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## normales_data : un tableau de données des normales pour les trous joués
##
## Valeur
##
## Un message d'erreur sera retourné s'il y a lieux.
##
## Exemple
##
## Vérif_Data(data, normales_data)
##
Vérif_Data <-
  function(data,
           normales_data = read.csv2("Data/normales.csv")) {
    # Présence de valeurs inférieures à 1 dans les données partielles.
    if (length(data[!is.na(data)][data[!is.na(data)] < 1]) != 0 |
        (typeof(unlist(data)) != "double")) {
      stop(
        paste(
          "Les données comportent une/des erreur(s)/",
          "valeur(s) invalide(s). NA, NULL, etc sont les valeurs manquantes",
          "acceptées. De plus, une valeur inférieur à 1 est une erreur"
        )
      )
    }
  }