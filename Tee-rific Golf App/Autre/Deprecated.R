#### tp, Pascal, Geneviève, Charles, Michaël
##
# Deprecated, Modèle retiré
#
#####
c(a_bn, b_bn) %<-%
  c(0, 0)

bayes_modèles <- function(data,
                          normales_data = read.csv2("normales.csv"),
                          model_B) {
  model_B <- c(model_B[1]) # seulement pour être consistent
  if ("BinN_Beta_NOR" %in% model_B) {
    if (a_bn == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = model_B)
    }
    # Mise en place des données
    normale <- rowSums(normales_data)

    data_bin_norm <-
      (Data_Norm(data, normales_data)[2:(length(normales_data) + 1)] *
         normale)

    # Calcule des paramètres et prédictions
    a_bn_b <-
      (a_bn[2] + length(normales_data) - rowSums(is.na(data_bin_norm)))
    b_bn_b <- (-b_bn[2] + rowSums(data_bin_norm, na.rm = TRUE))

    Pi <- (a_bn_b - 1) / (a_bn_b + b_bn_b)# * normale
    #p = a_bn_b / (a_bn_b + b_bn_b)
    #Pi = (1 - p) / p * normale

    # Remplacer les Na par la prédiction
    for (i in 1:length(data_bin_norm[, 1])) {
      data_bin_norm[i, ][is.na(data_bin_norm[i, ])] <- Pi[i]
    }

    # Remettre en ratio de coups de la normale
    data_bin_norm <- data_bin_norm / normale
    # Remettre en nombre de coups
    data_bin_norm <-
      data_bin_norm * (normales_data)[col(data_bin_norm)]

    Predicted <- rowSums(data_bin_norm)
  }
  if ("Bin_Bet_NOR_cm" %in% model_B) {
    if (a_norm == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = "Bin_Bet_NOR")
    }

    data_bin_norm <-
      (Data_Norm(data - 1,
                 normales_data - 1)[2:(length(normales_data) + 1)]
       * rowSums(normales_data - 1))

    bayes_cm_bin_norm <-
      cm(
        "bayes",
        data = data_bin_norm ,
        likelihood = "binomial",
        shape1 = a_norm,
        shape2 = b_norm,
        size = n_norm
      )

    Pi <- predict(bayes_cm_bin_norm)

    for (i in 1:length(data_bin_norm[, 1])) {
      data_bin_norm[i, ][is.na(data_bin_norm[i, ])] <- Pi[i]
    }

    # Remettre en ratio de la normale
    data_bin_norm <- data_bin_norm / rowSums(normales_data - 1)
    # Remettre en nombre de coups
    data_bin_norm <-
      data_bin_norm * (normales_data - 1)[col(data_bin_norm)] + 1

    Predicted <- rowSums(data_bin_norm)
  }
  if ("Norm_Norm_cm" %in% model_B) {
    if (sigma == 0) {
      bayes_paramètres(normales_data = normales_data, model_B = "Norm_Norm")
    }

    data_norm <-
      Data_Norm(data,
                normales_data)[2:(length(normales_data) + 1)]
    data_norm[is.na(data_norm)] <- ""

    bayes_cm_norm <- cm(
      "bayes",
      data = data_norm,
      likelihood = "normal",
      sd.lik = sqrt(sigma),
      mean = mu_0,
      sd = sqrt(sigma_0)
    )

    Pi <- predict(bayes_cm_norm)

    for (i in 1:length(data_norm[, 1])) {
      data_norm[i, ][is.na(data_norm[i, ])] <- Pi[i]
    }

    # Remettre en nombre de coups
    data_norm <-
      data_norm * (normales_data)[col(data_norm)]

    Predicted <- rowSums(data_norm)
  }
  unname(round(Predicted))
}
#####
bayes_paramètres <-
  function(data_complets =
             Data_Cor(Data_Tro(read.csv2("resultats-complets.csv"))),
           normales_data,
           model_B) {
    if ("BinN_Beta_NOR" %in% model_B) {
      data_bin_norm <-
        unlist(Data_Norm(data_complets,
                         normales_data)[2:(length(normales_data) + 1)],
               use.names = FALSE) * rowSums(normales_data)

      E_emp_X_norm <- mean(data_bin_norm)
      V_emp_X_norm <- var(data_bin_norm)

      foo <- function(a_bn) {
        b_bn = ((a_bn - 1 - a_bn * E_emp_X_norm) / E_emp_X_norm)

        ((a_bn - 2) / (a_bn + b_bn - 2) -
            2 * (a_bn - 1) / (a_bn + b_bn - 1) + 1 -
            ((a_bn - 2) / (a_bn + b_bn - 1)) ^ 2 +
            (a_bn - 2) / (a_bn + b_bn - 1)
          - V_emp_X_norm
        )
      }

      ##### findzeros cherche pas dans le bon environnement?!?!?!
      assign("foo", foo, envir = .GlobalEnv)
      # mauvaise solutions au problème, mais je vois pas pourquoi cela arrive

      a_bn <- unlist(findZeros(foo(a_bn) ~ a_bn), use.names = FALSE)
      #a_bn <- a_bn[which(abs(foo(a_bn) - 0) == min(abs(foo(a_bn) - 0)))]
      # Supprimer foo, parce qu'il n'aurait jamais du être global.
      rm(foo, envir = .GlobalEnv)

      b_bn <- ((a_bn - 1 - a_bn * E_emp_X_norm) / E_emp_X_norm)

      assign("a_bn", abs(a_bn) , envir = .GlobalEnv)
      assign("b_bn", abs(b_bn), envir = .GlobalEnv)
    }
  }