library(shiny)

shinyUI(fluidPage(
  fileInput(
    'datafile',
    'Choose CSV file',
    accept = c('csv', 'comma-separated-values', '.csv')
  ),
  tableOutput('table')
))