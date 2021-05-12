#### tp: Pascal, Geneviève, Charles, Michaël
###
### bayes_modèles
###
## Fonction calculant la prime bayesienne selon les oberservations précédentes
## pour différents modèles bayesiens.
## Voir : "http://www.ams.sunysb.edu/~zhu/ams570/Bayesian_Normal.pdf?
##        fbclid=IwAR0vNmkSsLEjEg2Ho8eF6iEM-y5VDBGHzrXn_g3PFwfwVJKdplFZH1mx3Z0"
##        pour notre source sur le modèle norm-norm.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## normales_data : un tableau de données des normales pour les trous joués.
##
## model_B : un vecteur des modèles bayesiens à prédire.
## (vecteur, pour être de même forme que bayes_paramètres(...), mais
## s'il y a une plus qu'une valeur dans la fonction seulement
## le premier modèle sera calculé). Les différents modèles sont "Norm_Norm",
## "Bin_Bet_PAR", "Bin_Bet_NOR" et "Poi_Gam_NOR". Les loi à priori et la loi de
## theta sont celles identifiées. "Nor" signifie que le modèle normalise les
## données, "Par" que les trous sont séparés en catégories selon les normales
## attendus (doivent être 3, 4 ou 5)
##
##
## (Les paramètres des modèles ne sont pas des arguments. Ils se retrouvent dans
## l'environnement global. Cela permet de recalculer seulement les paramètres
## nécessaires pour la prédiction voulue (ex: si les données complètes changent,
## les paramètres de tous les modèles aussi, mais seulement les paramètres du
## modèles de Bühlmann seraient recalculés, car c'est le modèle qui
## nous intéresserait).)
##
## Valeur
##
## Retourne une matrice des prédictions pour les trous non-joués.
##
## Exemple
##
## bayes_modèles(data, normales_data, model_B)
##
bayes_modèles <- function(data,
                          normales_data = read.csv2("Data/normales.csv"),
                          model_B = c("Bin_Bet_PAR")) {
  model_B <- c(model_B[1]) # seulement pour être consistent

  if ("Norm_Norm" %in% model_B) {
    if (Norm_Norm_para[1] == 0) {
      ## Recalcule des paramètres si nécéssaire.
      bayes_paramètres(normales_data = normales_data, model_B = model_B)
    }

    sigma <- Norm_Norm_para[1]
    sigma_0 <- Norm_Norm_para[2]
    mu_0 <- Norm_Norm_para[3]

    # Normalisé par rapport au échec, augmentent la précision de "Norm-Norm"
    data <- Data_Norm(data, normales_data)

    n = (length(normales_data) -
           rowSums(is.na(data[, 2:(length(normales_data) + 1)])))
    x_sum = rowSums(data[2:(length(normales_data) + 1)], na.rm = TRUE)

    mu_1 <- (mu_0 * sigma + x_sum * sigma_0) / (sigma + n * sigma_0)

    # Remplacer les NA par les valeurs prédites
    for (i in 1:length(data[, 1])) {
      data[i,][is.na(data[i,])] <- mu_1[i]
    }

    # Remettre les ratios par rapport aux trous prédits
    data[2:(length(normales_data) + 1)] <-
      data[2:(length(normales_data) + 1)] * (normales_data)[col(data)]

    data[data == 0] <- 1

    Predicted <- data[2:(length(normales_data) + 1)]
  }
  else if ("Bin_Bet_PAR" %in% model_B) {
    if (Bin_Bet_PAR_para[1] == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = model_B)
    }

    a_3 <- Bin_Bet_PAR_para[1]
    b_3 <- Bin_Bet_PAR_para[2]
    n_3 <- Bin_Bet_PAR_para[3]

    a_4 <- Bin_Bet_PAR_para[4]
    b_4 <- Bin_Bet_PAR_para[5]
    n_4 <- Bin_Bet_PAR_para[6]

    a_5 <- Bin_Bet_PAR_para[7]
    b_5 <- Bin_Bet_PAR_para[8]
    n_5 <- Bin_Bet_PAR_para[9]

    data_par_3 <-
      data[, 2:(length(normales_data) + 1)][, normales_data == 3]
    data_par_4 <-
      data[, 2:(length(normales_data) + 1)][, normales_data == 4]
    data_par_5 <-
      data[, 2:(length(normales_data) + 1)][, normales_data == 5]

    a_3_B <- (a_3 + rowSums(data_par_3, na.rm = TRUE))
    b_3_B <- (b_3 + n_3 * (sum(normales_data == 3) -
                             rowSums(is.na(data_par_3))) -
                rowSums(data_par_3, na.rm = TRUE))

    a_4_B <- (a_4 + rowSums(data_par_4, na.rm = TRUE))
    b_4_B <- (b_4 + n_4 * (sum(normales_data == 4) -
                             rowSums(is.na(data_par_4))) -
                rowSums(data_par_4, na.rm = TRUE))

    a_5_B <- (a_5 + rowSums(data_par_5, na.rm = TRUE))
    b_5_B <- (b_5 + n_5 * (sum(normales_data == 5) -
                             rowSums(is.na(data_par_5))) -
                rowSums(data_par_5, na.rm = TRUE))

    E_Par_3 = n_3 * a_3_B / (a_3_B + b_3_B)
    E_Par_4 = n_4 * a_4_B / (a_4_B + b_4_B)
    E_Par_5 = n_5 * a_5_B / (a_5_B + b_5_B)

    E_Par_3[E_Par_3 < 0] <- 1
    E_Par_4[E_Par_4 < 0] <- 1
    E_Par_5[E_Par_5 < 0] <- 1

    # Remplacer les NA par les valeurs prédites
    data_temp <- data[2:(length(normales_data) + 1)]
    for (i in 1:length(data_temp[, 1])) {
      data_temp[i, is.na(data_temp[i,]) &
                  normales_data == 3] <- E_Par_3[i]
      data_temp[i, is.na(data_temp[i,]) &
                  normales_data == 4] <- E_Par_4[i]
      data_temp[i, is.na(data_temp[i,]) &
                  normales_data == 5] <- E_Par_5[i]
    }

    Predicted <- data_temp
  }
  else if ("Bin_Bet_NOR" %in% model_B) {
    if (Bin_Bet_NOR_para[1] == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = model_B)
    }

    a_norm <- Bin_Bet_NOR_para[1]
    b_norm <- Bin_Bet_NOR_para[2]
    n_norm <- Bin_Bet_NOR_para[3]


    # Mise en place des données
    normale <- rowSums(normales_data)

    data_bin_norm <-
      (Data_Norm(data, normales_data)[2:(length(normales_data) + 1)] *
         normale)

    # Calcule des paramètres et prédictions
    a_norm_b = (a_norm + rowSums(data_bin_norm, na.rm = TRUE))
    b_norm_b = (b_norm + n_norm * (length(normales_data) -
                                     rowSums(is.na(data_bin_norm)))
                - rowSums(data_bin_norm, na.rm = TRUE))

    E_norm = n_norm * (a_norm_b / (a_norm_b + b_norm_b))

    # Remplacer les Na par la prédiction
    for (i in 1:length(data_bin_norm[, 1])) {
      data_bin_norm[i,][is.na(data_bin_norm[i,])] <- E_norm[i]
    }

    # Remettre en ratio de coups de la normale
    data_bin_norm <- data_bin_norm / normale
    # Remettre en nombre de coups
    data_bin_norm <-
      data_bin_norm * (normales_data)[col(data_bin_norm)]

    data_bin_norm[data_bin_norm == 0] <- 1


    Predicted <- data_bin_norm
  }
  else if ("Poi_Gam_NOR" %in% model_B) {
    if (Poi_Gam_NOR_para[1] == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = model_B)
    }

    lamda_P <- Poi_Gam_NOR_para[1]
    alpha_P <- Poi_Gam_NOR_para[2]

    # Mise en place des données
    normale <- rowSums(normales_data)

    data_bin_norm <-
      (Data_Norm(data, normales_data)[2:(length(normales_data) + 1)] *
         normale)

    # Calcule des paramètres et prédictions
    lamda_P_b = lamda_P + length(normales_data) - rowSums(is.na(data_bin_norm))

    alpha_P_b = (alpha_P + rowSums(data_bin_norm, na.rm = TRUE))

    E_norm = alpha_P_b / lamda_P_b

    # Remplacer les Na par la prédiction
    for (i in 1:length(data_bin_norm[, 1])) {
      data_bin_norm[i,][is.na(data_bin_norm[i,])] <- E_norm[i]
    }

    # Remettre en ratio de coups de la normale
    data_bin_norm <- data_bin_norm / normale
    # Remettre en nombre de coups
    data_bin_norm <-
      data_bin_norm * (normales_data)[col(data_bin_norm)]

    data_bin_norm[data_bin_norm == 0] <- 1

    Predicted <- data_bin_norm
  }

  unname(Predicted)
}
###
###
### bayes_paramètres
###
## Fonction calculant les paramètres empirique pour différents modèles
## bayesiens.
##
## Arguments
##
## complets_data : un tableau de données des trous joués pour chaque quatuor qui
##                 sert d'oberservations initales.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## model_B : un vecteur des modèles bayesiens dont les paramètres sont voulus.
## Les différents modèles sont "Norm_Norm", "Bin_Bet_PAR", "Bin_Bet_NOR" et
## "Poi_Gam_NOR". Les loi à priori et la loi de theta sont celles identifiées.
## "Nor" signifie que le modèle normalise les données, "Par" que les
## trous sont séparés en catégories selon les normales attendus (doivent être 3,
## 4 ou 5).
##
## Valeur
##
## (Les paramètres des modèles ne sont pas des valeurs retournées. Ils sont
## assignés dans l'environnement global pour être utilisé par les autres
## fonctions. Cela permet de recalculer seulement les paramètres nécessaires
## pour la prédiction voulue (ex.: si les données complètes changent,
## les paramètres de tous les modèles aussi, mais seulement les paramètres du
## modèles de Bühlmann seraient recalculés, car c'est le modèle qui
## nous intéresserait).)
##
## Exemple
##
## bayes_paramètres(complets_data, normales_data, model_B)
##
bayes_paramètres <-
  function(complets_data =
             Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv"))),
           normales_data,
           model_B) {
    if ("Norm_Norm" %in% model_B) {
      # Normalisé par rapport au échec, augmentent la précision de "Norm-Norm"
      data_temp <- Data_Norm(complets_data, normales_data)

      # Isoler les a et b des formules: V(X) = V(E(X|theta)) + E(V(X|theta))
      # et E(X) = E(E(X|theta)) => directement
      sigma_0 <- var(data_temp$Résultat_ronde_normalisé)

      # Moyenne d'une moyenne (équivalent, mais c'est plus rapide)
      mu_0 <- mean(data_temp$Résultat_ronde_normalisé)
      sigma <- var(unlist(data_temp[2:(length(normales_data) + 1)],
                          use.names = FALSE))

      assign("Norm_Norm_para",
             c(
               sigma = sigma,
               sigma_0 = sigma_0,
               mu_0 = mu_0
             ) ,
             envir = .GlobalEnv)
    }
    if ("Bin_Bet_PAR" %in% model_B) {
      data_par_3 <-
        unlist(complets_data[, 2:(length(normales_data) + 1)]
               [, normales_data == 3], use.names = FALSE)

      data_par_4 <-
        unlist(complets_data[, 2:(length(normales_data) + 1)]
               [, normales_data == 4], use.names = FALSE)

      data_par_5 <-
        unlist(complets_data[, 2:(length(normales_data) + 1)]
               [, normales_data == 5], use.names = FALSE)


      # Isoler les a et b des formules: V(X) = V(E(X|theta)) + E(V(X|theta))
      # et E(X) = E(E(X|theta))
      ### Pour les trous par 3
      n_3 <- max(data_par_3)
      E_emp_theta_3 <- mean(data_par_3) / n_3
      V_emp_theta_3 <-
        ((var(data_par_3) + n_3 * (E_emp_theta_3 ^ 2 - E_emp_theta_3)) /
           (n_3 ^ 2 - n_3))

      a_3 <- (E_emp_theta_3 * (1 - E_emp_theta_3 - V_emp_theta_3) /
                (V_emp_theta_3))

      b_3 <- a_3 / E_emp_theta_3 - a_3


      ### Pour les trous par 4
      n_4 <- max(data_par_4)
      E_emp_theta_4 <- mean(data_par_4) / n_4
      V_emp_theta_4 <-
        ((var(data_par_4) + n_4 * (E_emp_theta_4 ^ 2 - E_emp_theta_4)) /
           (n_4 ^ 2 - n_4))

      a_4 <- (E_emp_theta_4 * (1 - E_emp_theta_4 - V_emp_theta_4) /
                (V_emp_theta_4))

      b_4 <- a_4 / E_emp_theta_4 - a_4

      ### Pour les trous par 5
      n_5 <- max(data_par_5)
      E_emp_theta_5 <- mean(data_par_5) / n_5
      V_emp_theta_5 <-
        ((var(data_par_5) + n_5 * (E_emp_theta_5 ^ 2 - E_emp_theta_5)) /
           (n_5 ^ 2 - n_5))

      a_5 <- (E_emp_theta_5 * (1 - E_emp_theta_5 - V_emp_theta_5) /
                (V_emp_theta_5))

      b_5 <- a_5 / E_emp_theta_5 - a_5

      assign(
        "Bin_Bet_PAR_para",
        c(
          a_3 = abs(a_3),
          b_3 = abs(b_3),
          n_3 = n_3,
          a_4 = abs(a_4),
          b_4 = abs(b_4),
          n_4 = n_4,
          a_5 = abs(a_5),
          b_5 = abs(b_5),
          n_5 = n_5
        ) ,
        envir = .GlobalEnv
      )
    }
    if ("Bin_Bet_NOR" %in% model_B) {
      data_bin_norm <-
        unlist(Data_Norm(complets_data,
                         normales_data)[2:(length(normales_data) + 1)],
               use.names = FALSE) * rowSums(normales_data)

      # Isoler les a et b des formules: V(X) = V(E(X|theta)) + E(V(X|theta))
      # et E(X) = E(E(X|theta)) => directement
      n_norm <- max(data_bin_norm)
      E_emp_theta_norm <- mean(data_bin_norm) / n_norm
      V_emp_theta_norm <-
        ((
          var(data_bin_norm) + n_norm * (E_emp_theta_norm ^ 2 -
                                           E_emp_theta_norm)
        ) /
          (n_norm ^ 2 - n_norm))

      a_norm <-
        (E_emp_theta_norm * (1 - E_emp_theta_norm - V_emp_theta_norm) /
           (V_emp_theta_norm))

      b_norm <- a_norm / E_emp_theta_norm - a_norm

      assign("Bin_Bet_NOR_para",
             c(
               a_norm = abs(a_norm) ,
               b_norm = abs(b_norm),
               n_norm = n_norm
             ) ,
             envir = .GlobalEnv)
    }
    if ("Poi_Gam_NOR" %in% model_B) {
      data_bin_norm <-
        unlist(Data_Norm(complets_data,
                         normales_data)[2:(length(normales_data) + 1)],
               use.names = FALSE) * rowSums(normales_data)

      E_emp_X_norm <- mean(data_bin_norm)
      V_emp_X_norm <- var(data_bin_norm)

      lamda_P = E_emp_X_norm / (V_emp_X_norm - E_emp_X_norm)
      alpha_P = lamda_P * E_emp_X_norm

      assign("Poi_Gam_NOR_para",
             c(lamda_P = lamda_P, alpha_P = alpha_P) ,
             envir = .GlobalEnv)
    }
  }
###
###
### Bühlmann_modèles
###
## Fonction calculant la prime de Bühlmann selon les oberservations précédentes
## de deux façons différentes.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## mode : Soit "Mean" ou "Iter". Signifie la façon dont la prédiction sera
##        calculée. Mean signifie que la prédiction sera utilisé pour tout les
##        trous non-joués et Iter que la prédiction sera considéré comme une
##        observation pour la prédiction du trou suivant. Les deux modes ne
##        change pas les résultats, mais Iter est excessivement lent.
##
## (Les paramètres des modèles ne sont pas des arguments. Ils se retrouvent dans
## l'environnement global. Cela permet de recalculer seulement les paramètres
## nécessaires pour la prédiction voulue (ex.: si les données complètes
## changent, les paramètres de tous les modèles aussi, mais seulement les
##  paramètres du modèles de Bühlmann seraient recalculés, car c'est le modèle
## qui nous intéresserait).)
##
## Valeur
##
## Retourne une matrice des prédictions pour les trous non-joués.
##
## Exemple
##
## Bühlmann_modèles(data, normales_data, mode)
##
Bühlmann_modèles <- function(data,
                             normales_data = read.csv2("Data/normales.csv"),
                             mode = "Mean") {
  if (Bulh_para[1] == 0) {
    Bühlmann_paramètres(normales_data = normales_data)
  }

  m <- Bulh_para[1]
  K <- Bulh_para[2]

  if (mode == "Mean") {
    data <- Data_Norm(data, normales_data)

    is_na = rowSums(is.na(data[2:(length(normales_data) + 1)]))

    n = length(normales_data) - is_na
    z = n / (n + K)

    X_moy = rowMeans(data[2:(length(normales_data) + 1)], na.rm = TRUE)
    X_moy[is.nan(X_moy)] <- 0

    Pi <-
      ((z * X_moy) +
         (1 - z) * m)

    for (i in 1:length(data[, 1])) {
      data[i, ][is.na(data[i, ])] <- Pi[i]
    }

    # Remettre en nb de coups
    data[2:(length(normales_data) + 1)] <-
      (data[2:(length(normales_data) + 1)] *
         (normales_data)[col(data)])

    data[data == 0] <- 1

    Predicted <- data[2:(length(normales_data) + 1)]
  }
  if (mode == "Iter") {
    data <- Data_Norm(data, normales_data)
    is_na = rowSums(is.na(data[2:(length(normales_data) + 1)]))

    for (i in 1:length(data[, 1])) {
      n = length(normales_data) - is_na[i]

      while (n < length(normales_data)) {
        z = n / (n + K)

        X_moy = rowMeans(data[2:(length(normales_data) + 1)], na.rm = TRUE)
        X_moy[is.nan(X_moy)] <- 0

        Pi <-
          ((z * X_moy
            + (1 - z) * m))
        data[i,][is.na(data[i,])][1] <-
          unlist(Pi, use.names = FALSE)

        n = n + 1
      }
    }

    # Remettre en nb de coups
    data[2:(length(normales_data) + 1)] <-
      (data[2:(length(normales_data) + 1)] *
         (normales_data)[col(data)])

    data[data == 0] <- 1

    Predicted <- data[2:(length(normales_data) + 1)]
  }

  unname(Predicted)
}
###
###
### Bühlmann_paramètres
###
## Fonction calculant les paramètres pour un modèle de Bühlmann selon des
## oberservations initiales.
##
## Arguments
##
## complets_data : un tableau de données des trous joués pour chaque quatuor qui
##                 sert d'oberservations initales.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## Valeur
##
## (Les paramètres du modèle ne sont pas des valeurs "retournées". Ils sont
## assignés dans l'environnement global pour être utilisé par les autres
## fonctions. Cela permet de recalculer seulement les paramètres nécessaires
## pour la prédiction voulue (ex.: si les données complètes changent,
## les paramètres de tous les modèles aussi, mais seulement les paramètres du
## modèles de Bühlmann seraient recalculés, car c'est le modèle qui
## nous intéresse).)
##
## Exemple
##
## Bühlmann_paramètres(complets_data, normales_data)
##
Bühlmann_paramètres <-
  function(complets_data =
             Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv"))),
           normales_data) {
    data_norm <- Data_Norm(complets_data, normales_data)


    Bühl_mod <-
      cm(formula = ~ Game_ID, data = data_norm[1:(length(normales_data) + 1)])
    m <- unlist(Bühl_mod$means[1], use.names = FALSE)

    n <- unlist(Bühl_mod$weights[2], use.names = FALSE)[1]
    K <- (n - Bühl_mod$cred[1] * n) / Bühl_mod$cred[1]

    assign("Bulh_para", c(m = m, K = K) , envir = .GlobalEnv)
  }
###
###
### Bühlmann_Straub_modèles
###
## Fonction calculant la prime de Bühlmann selon les oberservations précédentes
## de deux façons différentes.
##
## Arguments
##
## data : un tableau de données des trous joués pour chaque quatuor.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## (Les paramètres des modèles ne sont pas des arguments. Ils se retrouvent dans
## l'environnement global. Cela permet de recalculer seulement les paramètres
## nécessaires pour la prédiction voulue (ex.: si les données complètes
## changent, les paramètres de tous les modèles aussi, mais seulement les
##  paramètres du modèles de Bühlmann seraient recalculés, car c'est le modèle
## qui nous intéresserait).)
##
## Valeur
##
## Retourne une matrice des prédictions pour les trous non-joués.
##
## Exemple
##
## Bühlmann_Straub_modèles(data, normales_data)
##
Bühlmann_Straub_modèles <- function(data,
                              normales_data = read.csv2("Data/normales.csv")) {
  if (Bulh_Str_para[1] == 0) {
    Bühlmann_Straub_paramètres(normales_data = normales_data)
  }

  m_s <- Bulh_Str_para[1]
  K_s <- Bulh_Str_para[2]

  data <- Data_Norm(data, normales_data)

  # Créer un tableau des poids de chaque trou joué pour chaque quatuor
  weights_data <- data[1:(length(normales_data))]
  names(weights_data) <- 1:length(normales_data)
  weights_data[1:(length(normales_data))] <- normales_data
  weights_data[is.na(data[2:(length(normales_data) + 1)])] <- NA

  # Créer un vecteur de la somme des poids pour chaque quatuor
  w_iS <- rowSums(weights_data, na.rm = TRUE)

  z_i <- w_iS / (w_iS + K_s)

  X_moy = rowMeans(data[2:(length(normales_data) + 1)], na.rm = TRUE)

  X_moy[is.nan(X_moy)] <- 0
  z_i[X_moy == 0] <- 0

  Pi <-
    ((z_i * X_moy +
        (1 - z_i) * m_s))

  for (i in 1:length(data[, 1])) {
    data[i,][is.na(data[i,])] <- Pi[i]
  }

  # Remettre en nb de coups
  data[2:(length(normales_data) + 1)] <-
    (data[2:(length(normales_data) + 1)] *
       (normales_data)[col(data)])

  data[data == 0] <- 1

  Predicted <- data[2:(length(normales_data) + 1)]

  unname(Predicted)
}
###
###
### Bühlmann_Straub_paramètres
###
## Fonction calculant les paramètres pour un modèle de Bühlmann-Staub selon des
## oberservations initiales.
##
## Arguments
##
## complets_data : un tableau de données des trous joués pour chaque quatuor qui
##                 sert d'oberservations initales.
##
## normales_data : un tableau de données des normales pour les trous joués ou
##                  de l'espérance selon les données complètes pour ces mêmes
##                  trous.
##
## Valeur
##
## (Les paramètres du modèle ne sont pas des valeurs "retournées". Ils sont
## assignés dans l'environnement global pour être utilisé par les autres
## fonctions. Cela permet de recalculer seulement les paramètres nécessaires
## pour la prédiction voulue (ex.: si les données complètes changent,
## les paramètres de tous les modèles aussi, mais seulement les paramètres du
## modèles de Bühlmann seraient recalculés, car c'est le modèle qui
## nous intéresse).)
##
## Exemple
##
## Bühlmann_Straub_paramètres(complets_data, normales_data)
##
Bühlmann_Straub_paramètres <-
  function(complets_data =
             Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv"))),
           normales_data) {
    # Créer un tableau des poids de chaque trou joué pour chaque quatuor
    weights_norm <- complets_data
    weights_norm[1:(length(normales_data))] <- (normales_data)
    names(weights_norm) <- 1:length(normales_data)

    # Créer un tableau des ratios par rapport aux poids de chaque trou joué
    # pour chaque quatuor
    data_ratio <- complets_data

    data_ratio[2:(length(normales_data) + 1)] <-
      (data_ratio[2:(length(normales_data) + 1)] /
         (normales_data)[col(data_ratio)])

    # Mettre les poids et ratio ensemble
    data_with_Weight <- cbind(data_ratio, weights_norm)

    # Créer le modèle avec cm
    Bühl_strau_mod <-
      cm(
        formula = ~ Game_ID,
        data = data_with_Weight,
        ratios = names(data_with_Weight[2:(length(normales_data) + 1)]),
        weights = 1:(length(normales_data))
      )

    # Extraire les paramètres
    m_s <- unlist(Bühl_strau_mod$means[1], use.names = FALSE)

    w <- unlist(Bühl_strau_mod$weights[2], use.names = FALSE)[1]
    K_s <- (w - Bühl_strau_mod$cred[1] * w) / Bühl_strau_mod$cred[1]

    assign("Bulh_Str_para", c(m_s = m_s, K_s = K_s), envir = .GlobalEnv)
  }