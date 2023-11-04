import streamlit as st
st.set_page_config(layout="wide")

from src.classes.DataGenerator import DataGenerator
from src.classes.DataLoader import DataLoader
from src.classes.DashBoardGenerator import DashBoardGenerator

from src.constants.path import LOAD_DATA_PATH

def main():
    data_loader = DataLoader(LOAD_DATA_PATH)
    data_loader.load_data(generate_category=False)
    dashboard_generator = DashBoardGenerator('Personal Financial Dashboard', data_loader)
    dashboard_generator.generate_filter()
    dashboard_generator.generate_big_numbers()
    chart_monthly_expenses, table_monthly_expenses = st.columns([2, 1])
    with chart_monthly_expenses:
        dashboard_generator.generate_montlhy_expenses_chart()
    with table_monthly_expenses:
        dashboard_generator.generate_dataframe_chart()
    agg_type, cateogries_number = st.columns([1, 1])
    summary_type = agg_type.selectbox('Select the type of summary', ('Average', 'Total'))
    categories_number = cateogries_number.slider('Select the number of categories', 1, 10, 5)
    bar_chart_total, pie_chart = st.columns([1, 1])
    
    with bar_chart_total:
        graph_type = str(summary_type).lower()
        dashboard_generator.generate_bar_chart(
            column="origin_amount",
            number_categories=categories_number,
            title=f"{summary_type} amount by category",
            height=500,
            type=graph_type)
    with pie_chart:
        dashboard_generator.generate_pie_chart(
            column="origin_amount",
            number_categories=categories_number,
            title=f"{summary_type} amount by category",
            height=500,
            type=graph_type)
    
    categories = st.multiselect('Select categories', dashboard_generator.filtered_df.category.unique(), default=dashboard_generator.filtered_df.category.unique())
    dashboard_generator.generate_line_chart(
        'origin_amount',
        categories,
        500)

    
if __name__ == '__main__':
    main()