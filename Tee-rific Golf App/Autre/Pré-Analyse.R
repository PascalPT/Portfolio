#### tp, Pascal, Geneviève, Charles, Michaël

complets_data <- read.csv2("resultats-complets.csv")
complets_data[is.na(complets_data)] <- 0

# Tous les résultats différents obtenus (domaine observé)
for (j in 2:19) {
  print(paste(
    "Tous les résultats différents obtenus pour le trous",
    j - 1,
    ":",
    toString(sort(unique(complets_data[, j])))
  ))
}
rm(j)
#Populations des résultats supérieurs à 12
for (i in 2:19) {
  maximum <- max(complets_data[-1, i])
  if (maximum > 12) {
    print(
      paste0(
        "Résultat maximal pour le trou: ",
        i - 1,
        " : ",
        maximum,
        " (quantité supérieur à 12 : ",
        as.character(length(complets_data[, i][complets_data[, i] > 12])),
        ")"
      )
    )
  }
  else{
    print(paste("Résultat maximal pour le trou: ", i - 1, " : ", maximum))
  }

}
rm(i, maximum)

# Gestion d'erreurs dans les données (pour l'histogramme)
source("Gestionnaire_Data.R", encoding = "UTF-8")

complets_data <- Data_Man(Data_Net(complets_data))

complets_data$Résultat_ronde <- rowSums(complets_data[, 2:19])

hist(
  complets_data$Résultat_ronde,
  main = "Graphique 1: Histogramme des résultats totaux d'une ronde pour un
  échantillon de 2000 quatuors",
  xlim = c(60, 110),
  xlab = "résultats totaux des quatuors",
  ylab = "Fréquence"
)

normal_data <- Data_Norm(complets_data)

hist(normal_data$Résultat_ronde_normalisé)