#### tp: Pascal, Geneviève, Charles, Michaël
###
source("Init.R", encoding = "UTF-8")
#################
#################
#
# Importe les données.
partiels_data <- read.csv2("Data/resultats-partiels.csv")
#
# Trouve les erreurs dans les données et le met dans un autre tableau pour
# garder le premier tableau sans modification.
partiels_corr_data <-
  Data_Tro(partiels_data, complètes = FALSE)
#
# Trouve le modèle le plus précis selon le nombre de trous joués  et l'affiche.
plus_précis = c()
for (kk in 1:17) {
  print(kk)
  x <- Vérif_Err(complets_data, normales_data, kk / 18)
  plus_précis <- append(plus_précis, c(kk = names(x[1])))
}
rm(kk, x)
names(plus_précis) <- 1:17
plus_précis
#
# Affiche le nombre de trous joués dans les données partielles dans un
# histogramme.
nb_miss <- rowSums(is.na(partiels_data[2:19]))
hist(rowSums(is.na(partiels_data[2:19])))
#
# On ne veut pas corriger les lignes où il n'y pas beaucoup d'informations.
# (Remplace par des Na, les erreurs où cela est le cas.)
for (rows in 1:length(partiels_corr_data[, 1])) {
  if (length(partiels_corr_data[rows, is.na(partiels_corr_data[rows,])])
      + sum(partiels_corr_data[rows, 2:19] == -Inf, na.rm = TRUE)
      < 9) {
    cols <- partiels_corr_data[rows,] == -Inf
    cols[is.na(cols)] <- FALSE
    partiels_corr_data[rows, cols] <- NA
  }
}
rm(rows, cols)
#
# Corrige les autres erreurs.
partiels_corr_data <-
  Data_Cor(partiels_corr_data[1:19], normales_data, 1)
#
# Recalcule les paramètres.
bayes_paramètres(normales_data = esp_normales_data, model_B = c("Norm_Norm"))
Bühlmann_paramètres(normales_data = esp_normales_data)
#
# Calcule les prédictions.
predict_partiels_bulh_data <- round(rowSums(
  Bühlmann_modèles(
    partiels_corr_data,
    normales_data = esp_normales_data,
    mode = "Mean"
  )
))
#
# Calcule les prédictions.
predict_partiels_norm_data <- round(rowSums(
  bayes_modèles(
    partiels_corr_data,
    model_B = c("Norm_Norm"),
    normales_data = esp_normales_data
  )
))
#
# Calcul le résultat de la ronde pour chaque quatuor.
predict_partiels_data <- predict_partiels_bulh_data
predict_partiels_data[nb_miss %in% c(4, 6, 13, 14, 15)] <-
  predict_partiels_norm_data[nb_miss %in% c(4, 6, 13, 14, 15)]
#
# Remet les noms des colonnes.
partiels_data$TOTAL <- predict_partiels_data
#
# Remonte pour déposer le fichier csv
setwd("..")
#
# Écrie le fichier csv.
write.table(
  partiels_data,
  file = "resultats-partiels.csv",
  na = "",
  fileEncoding = "UTF-8",
  row.names = FALSE,
  sep = ";",
  dec = "."
)
#
# Redescent pour que le script soit réutilisable.
setwd("prototype")