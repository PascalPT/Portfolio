#### tp: Pascal, Geneviève, Charles, Michaël
######### ini/lib/data/source
{
  #  Essaye de charger les packages, si échec l'installe, puis le charge
  packages = c("actuar")#, "shiny")
  for (package in packages) {
    if (!require(package ,
                 character.only = TRUE,
                 warn.conflicts = FALSE)) {
      install.packages(package , dependencies = TRUE)
      require(package ,
              character.only = TRUE,
              warn.conflicts = FALSE)
      # Pas besoin de else => pour évaluer le if le package doit-être chargé
    }
  }
  rm(packages , package)
  ###
  ###
  ### Fichier des fonctions du tp
  source("Gestionnaire_Data.R", encoding = "UTF-8")
  source("Modèles.R", encoding = "UTF-8")
  source("Vérifications.R", encoding = "UTF-8")

  # Initialisation des paramètres
  #######################################
  # Norm-Norm (normalisée)
  Norm_Norm_para <- c(sigma = 0,
                      sigma_0 = 0,
                      mu_0 = 0)

  # Bin - Beta (Par 3,4,5)
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

  # Bin - Beta (normalisée)
  Bin_Bet_NOR_para <- c(a_norm = 0 ,
                        b_norm = 0,
                        n_norm = 0)


  # Poisson - Gamma (normalisée)
  Poi_Gam_NOR_para <- c(lamda_P = 0, alpha_P = 0)

  #################################
  # Bulhmann non-para. (normalisée)
  Bulh_para <- c(m = 0, K = 0)

  #################################
  # Bulhmann-str
  Bulh_Str_para <- c(m_s = 0, K_s = 0)

  #################################
  # Erreur abs

  Err_préd <- c(
    Norm_Norm = NA,
    Bin_Bet_PAR = NA,
    Bin_Bet_NOR = NA,
    Poi_Gam_NOR = NA,
    Bulh_Mean = NA,
    Bulh_str = NA
  )

  Err_préd <- as.data.frame(matrix(Err_préd, nrow = 1,
                                   dimnames = list(c(1),
                                                   names(Err_préd))))
}
#################
#################
setwd("..")

complets_data <-
  Data_Cor(Data_Tro(read.csv2("Data/resultats-complets.csv")))

normales_data <- read.csv2("Data/normales.csv")
Vérif_Norm(normales_data)

esp_normales_data <- normales_data

esp_normales_data[1:length(normales_data)] <-
  colMeans(complets_data[2:(length(normales_data) + 1)])