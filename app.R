#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

required_packages <- c(
    "shiny",
    "DT"
)

# Install or load dependencies
for (package in required_packages) {
    if (!require(package, character.only = TRUE)) {
        install.packages(package)
        library(package, character.only = TRUE)
    }
}

# Read in data
data <- read.table(
    "./files/results.tsv", header = TRUE, sep = "\t", check.names = FALSE
)

# UI component
ui <- navbarPage(
    "Precision Biomarker Laboratory",
    tabPanel(
        "Post-Translational Modifications Browser",
        sidebarLayout(
            sidebarPanel(
                textInput(
                    "protein_name",
                    "Protein Name:",
                    value = "",
                    placeholder = "(e.g. P00738)"
                ),
                textInput(
                    "full_peptide_name",
                    "Full Peptide Name:",
                    value = "",
                    placeholder = "(e.g. L(UniMod:7)GGHL(UniMod:7)DAK)"
                ),
                downloadButton("download", "Download as TSV"),
                width = 2
            ),
            mainPanel(DT::dataTableOutput("records"), width = 10)
        )
    )
)

# Server componenet
server <- function(input, output) {
    datatable_input <- reactive({
        dt <- data

        # Filter by protien name
        if (input$protein_name != "") {
            dt <- dt[dt$ProteinName == input$protein_name, ]
        }

        # Filter by full peptide name
        if (input$full_peptide_name != "") {
            dt <- dt[dt$FullPeptideName == input$full_peptide_name, ]
        }

        return(dt)
    })

    output$download <- downloadHandler(
        filename <- function() {
            paste("data-", Sys.Date(), ".tsv", sep="")
        },
        content <- function(file) {
            write.table(datatable_input(), file, sep = "\t", row.names = FALSE)
        }
    )

    output$records <- DT::renderDataTable({
        datatable_input()
    }, options = list(pageLength = 25))
}

# Bind UI and server to an application
shinyApp(ui = ui, server = server)
