#### tp: Pascal, Geneviève, Charles, Michaël
###
###
### quiet
###
### Source
### pour quiet (rmarkdown, retire les outputs)
### (source : "https://r.789695.n4.nabble.com/
### Suppressing-output-e-g-from-cat-td859876.html")
###
###
## Fonction effaçant les messages d'éxecutions.
##
## Arguments
##
## x : Ligne de codes quelconques, fonctions, etc; à éxecuter.
##
## Valeur
##
## Ne retourne rien. Efface les messages d'éxecutions.
##
## Exemple
##
## quiet(x)
##
quiet <- function(x) {
  sink(tempfile())
  on.exit(sink())
  invisible(force(x))
}

## Initialisation initale des paramètres et des données
setwd("Scripts")

quiet(source("Init.R",
             encoding = "UTF-8"))

ui <- fluidPage(
  ## Titre
  titlePanel("TP - Prédictions"),

  withMathJax(),


  ## Barre latérale avec les contrôles
  sidebarLayout(
    sidebarPanel(
      h4("Modèle recommandé: Modèle de Bühlmann"),
      helpText(
        "Dans la plus part des cas, c'est le modèle le plus précis. Dans ce
        modèle, on considère le ratio des scores obtenus à chaque trou par
        rapport à l'espérance pour chaque trou."
      ),
      helpText("$$K = \\frac{\\hat{s}^2}{\\hat{a}}$$"),
      helpText(
        "\\(\\hat{s}^2\\) est la variance intra, ou l'espérance de la variance
        de toutes les équipes"
      ),
      helpText(
        "\\(\\hat{a}\\) est la variance inter, ou la variance de l'espérance de
        toutes les équipes"
      ),
      helpText("La prédiction peut alors être faite avec:"),

      helpText(
        "$$\\hat{\\pi}_{n+1} = \\frac{\\sum_{t=1}^{n} \\pi_t}{n+\\hat{s}^2/
        \\hat{a}}+ \\frac{\\hat{s}^2/\\hat{a}}{n+\\hat{s}^2/\\hat{a}}\\times
        \\hat{m}$$"
      ),

      helpText("Voir en bas à droite pour plus d'information."),

      radioButtons(
        "modele",
        "Modèle Choisis",
        c(
          "Bayésien (Binomiale-Beta [Par type de trou])" =
            "bayes_Bin_Bet_PAR",
          "Bayésien (Binomiale-Beta [Normalisé])" =
            "bayes_Bin_Bet_NOR",
          "Bayésien (Normale-Normale)" =
            "bayes_Norm_Norm",
          "Bayésien (Poisson-Gamma)" =
            "bayes_Poi_Gam_NOR",

          "Bühlmann" = "buhl",
          "Bühlmann-Straub" = "buhl_str"
        ),
        selected = "buhl"
      ),
      numericInput("trou1", h3("Score trou 1"), value = NA, min = 1),
      numericInput("trou2", h3("Score trou 2"), value = NA, min = 1),
      numericInput("trou3", h3("Score trou 3"), value = NA, min = 1),
      numericInput("trou4", h3("Score trou 4"), value = NA, min = 1),
      numericInput("trou5", h3("Score trou 5"), value = NA, min = 1),
      numericInput("trou6", h3("Score trou 6"), value = NA, min = 1),
      numericInput("trou7", h3("Score trou 7"), value = NA, min = 1),
      numericInput("trou8", h3("Score trou 8"), value = NA, min = 1),
      numericInput("trou9", h3("Score trou 9"), value = NA, min = 1),
      numericInput("trou10", h3("Score trou 10"), value = NA, min = 1),
      numericInput("trou11", h3("Score trou 11"), value = NA, min = 1),
      numericInput("trou12", h3("Score trou 12"), value = NA, min = 1),
      numericInput("trou13", h3("Score trou 13"), value = NA, min = 1),
      numericInput("trou14", h3("Score trou 14"), value = NA, min = 1),
      numericInput("trou15", h3("Score trou 15"), value = NA, min = 1),
      numericInput("trou16", h3("Score trou 16"), value = NA, min = 1),
      numericInput("trou17", h3("Score trou 17"), value = NA, min = 1),
      numericInput("trou18", h3("Score trou 18"), value = NA, min = 1)
    ),

    ## Graphique et résultats en format texte
    mainPanel(
      h2("Prévision"),

      h3("On prévoit que l'équipe aura les résultats suivants:"),

      htmlOutput("SUM"),

      tags$hr(style = "border-color: black;"),

      dataTableOutput("TABLEAU"),

      actionButton("Err_Abs", "Écart absolu moyen des modèles"),

      numericInput(
        "m_mult",
        h3("Nombre de trous joués"),
        value = 6,
        min = 0,
        max = 18
      ),

      htmlOutput("Err_abs"),

      helpText(" "),

      helpText(
        "\\begin{aligned}
          \\hat{m} = \\bar{S} = \\frac{1}{In} \\sum_{i=1}^{I}
          \\sum_{t=1}^{n}S_{it} && \\hat{s}^2 = \\frac{1}{I(n-1)}
          \\sum_{i=1}^{I} \\sum_{t=1}^{n}(S_{it} - \\bar{S_i})^2
        \\end{aligned}"
      ),

      helpText(" "),

      helpText(
        "\\begin{aligned}
          \\hat{a} = \\frac{1}{I-1}\\sum_{i=1}^{I}(\\bar{S}_i -
          \\bar{S})^2 - \\frac{\\hat{s}^2}{n} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned} \\bar{S} \\text{: moyenne des ratios à partir de
        données complètes} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned} S_{it}\\text{: le ratio de la } i^e
      \\text{équipe au } t^e \\text{trou} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned} \\bar{S_i}\\text{: le ratio moyen de la } i^e
      \\text{équipe aux normales} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned}
        \\hat{\\pi}_{n+1} \\text{: le ratio d'un quatuor au } (n+1)^e
        \\text{ trou} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned} \\pi_t \\text{: le ratio du quatuor au trou t}
        \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned} \\hat{m} \\text{: moyenne des rondes à partir
               de données complètes} \\end{aligned}"
      ),

      helpText(
        "\\begin{aligned}
         \\text{n: nombre de trous joués} \\end{aligned}"
      ),

      helpText("\\begin{aligned} \\text{I: nombre de quatuors} \\end{aligned}")

    )
  )
)
##
##
## création du websocket
server <- function(input, output) {
  ## Mettre tous les trous déjà joués par une équipe dans un seul vecteur

  score_équipe <- reactive({
    scores <-
      c(
        Game_id = 1,
        input$trou1,
        input$trou2,
        input$trou3,
        input$trou4,
        input$trou5,
        input$trou6,
        input$trou7,
        input$trou8,
        input$trou9,
        input$trou10,
        input$trou11,
        input$trou12,
        input$trou13,
        input$trou14,
        input$trou15,
        input$trou16,
        input$trou17,
        input$trou18
      )

    scores <- as.data.frame(matrix(scores, nrow = 1))

    ## fun
    ##
    ## fonction temporaire pour rapply qui remplace les NaN par des Na.
    ##
    ## Arguments
    ##
    ## fu : objet contenant des NaN à remplacer par des NA
    ##
    ## Valeur
    ##
    ## Ne retourne rien. Remplace les NaN par des NA dans l'objet.
    ##
    ## Exemple
    ##
    ## fun(fu)

    fun <- function(fu) {
      ifelse(is.nan(fu), NA, fu)
    }
    scores <- rapply(scores, fun, how = "replace")

    rm(fun)

    Vérif_Data(scores, normales_data)

    scores

  })


  ## Calcul de la prévision

  prev <- reactive({
    data <- score_équipe()

    if (input$modele == "bayes_Bin_Bet_PAR") {
      previ <- bayes_modèles(data[1:(length(normales_data) + 1)],
                             model_B = c("Bin_Bet_PAR"),
                             normales_data = normales_data)
    }
    else if (input$modele == "bayes_Bin_Bet_NOR") {
      previ <- bayes_modèles(data[1:(length(normales_data) + 1)],
                             model_B = c("Bin_Bet_NOR"),
                             normales_data = esp_normales_data)
    }
    else if (input$modele == "bayes_Norm_Norm") {
      previ <- bayes_modèles(data[1:(length(normales_data) + 1)],
                             model_B = c("Norm_Norm"),
                             normales_data = esp_normales_data)
    }
    else if (input$modele == "bayes_Poi_Gam_NOR") {
      previ <- bayes_modèles(data[1:(length(normales_data) + 1)],
                             model_B = c("Poi_Gam_NOR"),
                             normales_data = esp_normales_data)
    }

    else if (input$modele == "buhl") {
      previ <- Bühlmann_modèles(data[1:(length(normales_data) + 1)],
                                normales_data = esp_normales_data)
    }
    else if (input$modele == "buhl_str") {
      previ <-
        Bühlmann_Straub_modèles(data[1:(length(normales_data) + 1)],
                                normales_data = esp_normales_data)
    }
    round(unlist(previ[1, ], use.names = FALSE))
  })

  ## Mise en forme des résultats

  table <- reactive({
    scores <- unlist(score_équipe()[1, 2:19], use.names = FALSE)

    Prediction <- numeric(18)
    Prediction[!is.na(scores)] <- "Joué"
    Prediction[Prediction == 0] <- "Simulé"
    data <-
      data.frame(Trou = 1:18,
                 Résultat = prev(),
                 Type = Prediction)
  })

  ## Erreur moyenne absolue

  observeEvent(input$Err_Abs, {
    m_mult <- suppressWarnings(as.numeric(input$m_mult))

    if (is.na(m_mult)) {
      m_mult <- -1
    }

    if (m_mult > length(normales_data) | m_mult < 0) {
      # Aurait dû être un stop, mais le mauvais environement est arrêter.
      #stop("Le nombre de trous joués est invalides.")
      Err_TxT <-
        paste0("<p style='color:red'> Le nombre de trous joués est",
               " invalides.</p>")

      output$Err_abs <- renderText({
        Err_TxT
      })
      return()
    }
    Vérif_complèts(complets_data = complets_data, normales_data = normales_data)
    Vérif_Err(
      complets_data = complets_data,
      normales_data = normales_data,
      m_multiple = round(m_mult) / length(normales_data)
    )

    Err_TxT <- paste0(
      "Erreur absolue moyenne par modèles: Binomiale-Beta [Par] = ",
      Err_préd$Bin_Bet_PAR ,
      ", ",
      "Binomiale-Beta [Nor.] = ",
      Err_préd$Bin_Bet_NOR ,
      ", ",
      "Normale-Normale = ",
      Err_préd$Norm_Norm,
      ", ",
      "Poisson-Gamma = ",
      Err_préd$Poi_Gam_NOR ,
      ", ",
      "Bühlmann = ",
      Err_préd$Bulh_Mean ,
      ", ",
      "Bühlmann-Straub = ",
      Err_préd$Bulh_str
    )

    output$Err_abs <- renderText({
      Err_TxT
    })
  })

  ## Affichage des valeurs prédites et de leurs sommes

  output$TABLEAU <- renderDataTable(table())

  output$SUM <- renderText({
    paste("<p style='font-size:25px'><b style='color:green'> Score final de
          l'équipe prédit:", sum(prev()), "</b></p>")
  })

}
##
## Application
shinyApp(ui = ui, server = server)