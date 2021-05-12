library(shiny)
library(ggplot2)

shinyServer(function(input, output, session) {
  dataframe <- reactive({
    if (is.null(input$datafile))
      return(NULL)
    data <- read.csv2(input$datafile$datapath)
    data <- data[1:4, 1:4]
    data
  })
  output$table <- renderTable({
    dataframe()
  })
})