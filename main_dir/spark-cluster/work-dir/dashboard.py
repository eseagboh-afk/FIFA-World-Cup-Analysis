import os 

import pandas as pd
import plotly.express as px 
from dash import Dash, Input, Output, callback, dcc, html, dash_table 
from dynaconf import Dynaconf
from sqlalchemy import create_engine
from etl import Transformer, ETLProcessor

parent_dir = os.path.dirname(__file__)

settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
engine = create_engine(settings.ENGINE_URL, echo=False)
print(engine)


def build_engine():
    settings = Dynaconf(envvar_prefix="DB", load_dotenv=True)
    return create_engine(settings.ENGINE_URL, echo=False)
    
engine = build_engine()

with engine.begin() as connection:

    data_table_query = """SELECT * FROM countries"""
    data_table_df = pd.read_sql(data_table_query, connection)

    gdp_scatter_query = """SELECT c.country_id, c.country_name, c.total_matches_won, c.total_matches_played, e.avg_total_gdp FROM countries as c
    INNER JOIN economic_status as e on e.country_id = c.country_id"""
    gdp_scatter_df = pd.read_sql(gdp_scatter_query, connection)

    gdp_scatter = px.scatter(gdp_scatter_df, x='avg_total_gdp', y='total_matches_won', color='country_name',
                             size='total_matches_played', title='Total World Cup Matches Won vs. Avg Total GDP')
    
    goals_scatter_query = """SELECT c.country_id, c.country_name, c.total_goals_scored, e.avg_international_liquidity, e.avg_total_gdp FROM countries as c
    INNER JOIN economic_status as e on e.country_id = c.country_id"""
    goals_scatter_df = pd.read_sql(goals_scatter_query, connection)
    goals_scatter = px.scatter(goals_scatter_df, x='avg_international_liquidity', y='total_goals_scored', color='country_name',
                               size='avg_total_gdp', title='Total World Cup Match Goals Scored vs. Avg International Liquidity')
    
    top_performers_query = """SELECT c.country_id, c.country_name, c.total_matches_won, e.avg_total_gdp FROM countries as c
    INNER JOIN economic_status as e on e.country_id = c.country_id ORDER BY total_matches_won DESC LIMIT 10"""
    top_performers_df = pd.read_sql(top_performers_query, connection)
    top_performers_bar = px.bar(top_performers_df.sort_values("total_matches_won", ascending=False),
                                x='country_name', y='total_matches_won', color='avg_total_gdp', title='Top Performing Countries')
    
    worst_performers_query = """SELECT c.country_id, c.country_name, c.total_matches_won, c.total_matches_played, e.avg_total_gdp FROM countries as c
    INNER JOIN economic_status as e on e.country_id = c.country_id WHERE c.total_matches_played > 0 ORDER BY total_matches_won ASC LIMIT 20"""

    worst_performers_df = pd.read_sql(worst_performers_query, connection)
    worst_performers_bar = px.scatter(worst_performers_df,x='country_name', y='total_matches_won', 
                                      color='country_name', size='avg_total_gdp', title='Worst Performing Countries')
    
    matches_distribution_query = """SELECT country_id, country_name, total_matches_played FROM countries"""

    matches_distribution_df = pd.read_sql(matches_distribution_query, connection)
    matches_distribution_plot = px.box(matches_distribution_df, y='total_matches_played', title='Total Number of Matches Played')

    champions_gdp_query = """SELECT count(ch.country_id) as world_cups_won, c.country_name, e.avg_total_gdp FROM world_cup_champions as ch
    INNER JOIN countries as c on c.country_id = ch.country_id
    INNER JOIN economic_status as e on e.country_id = c.country_id
    GROUP BY (c.country_name, e.avg_total_gdp)"""
    champions_gdp_df = pd.read_sql(champions_gdp_query, connection)
    champions_gdp_bar = px.bar(champions_gdp_df.sort_values('avg_total_gdp', ascending=False), x='country_name',y='world_cups_won',
                               color='avg_total_gdp', title='Avg GDP of World Cup Winners')



app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Comparison of World Cup Statistics and Country Infrastructure"),
        html.H2("Snapshot of Dataset"),
        dash_table.DataTable(
            data = data_table_df.to_dict("records"), page_size = 10, sort_action="native"
        ),

        html.P("This dataset was created by extracting World Cup matches from a Kaggle dataset of all FIFA regulated matches"),
        html.P("The cut off date for this analysis is June 17, 2026"),
        html.A("Click here to view data", href='https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017/data?select=results.csv'),

        html.H2('Quick Facts:'),

        html.H3('Number of completed World Cup Tournaments: 22'),
        html.H3('Number of World Cup matches played since 1930: 988'),
        html.H3('Number of World Cup goals scored since 1930: 2801'),
        html.H3('Number of unique countries to qualify for the World Cup: 86'),
        html.H3('Average World Cup matches by country: 23'),
        html.H3('Average of the average total GDP of World Cup qualifiers: $298,497,631.87'),
        html.H3('Average of the average international liquidity of World Cup qualifiers: $28,512.79'),


        html.H2('Considerations:'),

        html.H3('Average total GDP is calculated over time from 1950 to 2022'),
        html.H3('Average international liquidity is calculated over time from 1950 to 2025'),
        html.H3('There is a World Cup tournament currently occurring; match and goal statistics are current as of June 17, 2026'),


        html.H2("Total Number of Matches Played"),
        dcc.Graph(id='Matches Distribution Plot', figure=matches_distribution_plot),
       

        html.H2("World Cup Matches Won vs. Avg Total GDP by Country:"),
        dcc.Graph(id='gdp_scatter', figure=gdp_scatter),

        html.H2("Total Goals Scored vs. Avg Total International Liquidity by Country:"),
        dcc.Graph(id='goals_scatter', figure=goals_scatter),

        html.H2("Top 10 Performing Countries:"),
        dcc.Graph(id='Top Performing Countries', figure=top_performers_bar),

        html.H2("Worst Performing Countries:"),
        dcc.Graph(id='Worst Performing Countries', figure=worst_performers_bar),

        html.H2("Average Total GDP of World Cup Winners"),
        dcc.Graph(id='Average Total GDP of World Cup Winners', figure=champions_gdp_bar),

    ]
)

if __name__ == "__main__":
    app.run(debug=True)
