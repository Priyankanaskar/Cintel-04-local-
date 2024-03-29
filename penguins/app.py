# import libraries----------------------------------------------------------------------------------------------------------------------------------
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import shinyswatch


# Theme------------------------------------------------------------------------------------------------------------------------------------------------------------
shinyswatch. theme.superhero()

# This package provides the Palmer Penguins dataset----------------------------------------------------------------------------------------------

from shiny import reactive, render, req
import seaborn as sns
import pandas as pd
import palmerpenguins

# Use the built-in function to load the Palmer Penguins dataset-----------------------------------------------------------------------------------------------
import seaborn as sns
penguins = sns.load_dataset("penguins")
penguins_df = load_penguins()



# Use the built-in function to load the Palmer Penguins dataset-----------------------------------------------------------------------------------------------------------
penguins_df = palmerpenguins.load_penguins()
penguins_df_r = penguins_df.rename(columns={"bill_depth_mm": "Bill Depth (mm)", "bill_length_mm": "Bill Length (mm)", 
"flipper_length_mm": "Flipper Length (mm)", "body_mass_g": "Body Mass (g)", "species": "Species", "island": "Island", "sex": "Sex", "year": "Year"})

# Name the page ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ui.page_opts(title="Priyanka's Penguin Dashboard", fillable=False)
color_map = {"Adelie": "blue", "Gentoo": "green", "Chinstrap": "red"}
#Shiny UI sidebar for user interaction------------------------------------------------------------------------------------------------------------------------------------------------

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    

# Create a dropdown input to choose a column -----------------------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_selectize("selected_attribute", "Body Measurement", choices=["Bill Length (mm)", "Bill Depth (mm)", "Flipper Length (mm)", "Body Mass (g)"]) 
    
# Create a numeric input for the number of Plotly histogram bins----------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30)
    
# Create a slider input for the number of Seaborn bins---------------------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 20)
    
# Create a checkbox group input to filter the species-------------------------------------------------------------------------------------------------------------------------------------------------
    ui.input_checkbox_group("selected_species_list", "Selected Species of Penguins", 
                            ["Adelie", "Gentoo", "Chinstrap"], selected="Adelie", inline=False)
    
 # Use ui.input_checkbox_group() to create a checkbox group input to filter the islands--------------------------------------------------------------------
    ui.input_checkbox_group(
        "selected_islands",
        "Islands in Graphs",
        ["Torgersen", "Biscoe", "Dream"],
        selected=["Torgersen", "Biscoe", "Dream"],
        inline=False,
    )
    
# Add a horizontal rule to the sidebar----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ui.hr() 

# Add a hyperlink to the sidebar------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    ui.h6("Links:")

    ui.a(
        "GitHub Source",
        href="https://github.com/Priyankanaskar/Cintel-04-Local/blob/main/penguins/app.py",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/Priyankanaskar/Cintel-04-Local",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")

    ui.a(
        "PyShiny Express",
        href="hhttps://shiny.posit.co/blog/posts/shiny-express/",
        target="_blank",
        
    )
    
    ui.a(
        "See the Code",
        href="https://shiny.posit.co/py/docs/user-interfaces.html#basic-dashboard",
        target="_blank",
    )
    ui.a(
        "Output: DataGrid",
        href="https://shiny.posit.co/py/components/outputs/datatable/",
        target="_blank",
    )
    ui.a(
        "Output: DataTable",
        href="https://shiny.posit.co/py/components/outputs/datatable/",
        target="_blank",
    )
    ui.a(
        "Output: Plotly Scatterplot",
        href="https://shiny.posit.co/py/components/outputs/plot-plotly/",
        target="_blank",
    )
    
    ui.a(
        "Output: Seaborn Histogram",
        href="https://shiny.posit.co/py/components/outputs/plot-seaborn/",
        target="_blank",
    )
   
# create a layout to include 2 cards with a data table and data grid------------------------------------------------------------------------------------------------------------------------------
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable( filtered_data())

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid( filtered_data())
            
# Plot Charts----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ui.input_select("x", "Variable:",
                choices=["bill_length_mm", "bill_depth_mm"])
ui.input_select("dist", "Distribution:", choices=["hist", "kde"])
ui.input_checkbox("rug", "Show rug marks", value = False)


## Column--------------------------------------------------------------------------------------------------------------------------------------------


@render.plot
def displot():
    sns.displot(
        data=penguins, hue="species", multiple="stack",
        x=input.x(), rug=input.rug(), kind=input.dist())


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Create Scatter plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Penguins Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        return px.scatter(filtered_data(), x="Flipper Length (mm)", y="Bill Length (mm)", color="Species", 
                          facet_row="Species", facet_col="Sex", title="Penguin Scatterplot")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pie Chart plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Pie Chart: Body Mass")

    @render_plotly
    def plotly_pie():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Island", title="Body mass on Islands")
        return pie_chart

    @render_plotly
    def plotly_pie_s():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Species", title="Body mass from Species")
        return pie_chart
        
# Card view for visualization---------------------------------------------------------------------------------------------------------------------------------------------------------

from shiny import App, ui

app_ui = ui.page_fillable(
    ui.layout_column_wrap(  
        ui.card("Card 1"),
        ui.card("Card 2"),
        ui.card("Card 3"),
        ui.card("Card 4"),
       width="2px",
        length="2px"
    ),
)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df_r[penguins_df_r["Species"].isin(input.selected_species_list())]
