import streamlit as st
st.set_page_config(layout="wide")

from src.classes.DataGenerator import DataGenerator
from src.classes.DataLoader import DataLoader
from src.classes.DashBoardGenerator import DashBoardGenerator

from src.constants.path import LOAD_DATA_PATH

def main():
    data_loader = DataLoader(LOAD_DATA_PATH)
    data_loader.load_data(generate_category=False)
    dataframe = data_loader.get_card_transactions_dataframe()
    money_in = data_loader.get_money_in()
    money_out = data_loader.get_money_out()
    balance = round(money_in - money_out, 2)
    monthly_avg_spendings = data_loader.get_monthly_avg_spendings()
    dashboard_generator = DashBoardGenerator('Personal Financial Dashboard', dataframe)
    dashboard_generator.generate_side_bar()
    kpi_container = st.container()
    with kpi_container:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            dashboard_generator.generate_card("Money In", money_in, None)
        with kpi2:
            dashboard_generator.generate_card("Money Out", money_out, None)
        with kpi3:
            dashboard_generator.generate_card("Balance", balance, None)
        with kpi4:
            dashboard_generator.generate_card("Avg. Spending", monthly_avg_spendings, None)

    st.subheader('Amount by category')
    summary_type = st.selectbox(
    'Select the type of summary',
    ('Total', 'Average'))
    print(summary_type)
    bar_chart_container = st.container()

    with bar_chart_container:
        bar_chart_total, pie_chart = st.columns([1, 1])
        graph_type = str(summary_type).lower()
        with bar_chart_total:
            dashboard_generator.generate_bar_chart(
                "origin_amount",
                None,
                5.65,
                type=graph_type)
        with pie_chart:
            dashboard_generator.generate_pie_chart(
                'origin_amount',
                None,
                4,
                type=graph_type)

    dashboard_generator.generate_line_chart('origin_amount', 'Time series: amount by category', 1.5)

    
if __name__ == '__main__':
    main()