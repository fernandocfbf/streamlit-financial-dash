import streamlit as st
st.set_page_config(layout="wide")

from src.classes.DataGenerator import DataGenerator
from src.classes.DataLoader import DataLoader
from src.classes.DashBoardGenerator import DashBoardGenerator

from src.constants.path import LOAD_DATA_PATH

def main():
    data_loader = DataLoader(LOAD_DATA_PATH)
    dataframe = data_loader.load_data(generate_category=False)
    dashboard_generator = DashBoardGenerator('Personal Financial Dashboard', dataframe)
    dashboard_generator.generate_side_bar()
    kpi_container = st.container()
    with kpi_container:
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            dashboard_generator.generate_card("Money In", 1255.02, None)
        with kpi2:
            dashboard_generator.generate_card("Money Out", 1233.00, None)
        with kpi3:
            dashboard_generator.generate_card("Balance", 22.02, None)
        with kpi4:
            dashboard_generator.generate_card("Savings", 100.00, None)

    #dashboard_generator.generate_raw_data()
    data_container = st.container()
    with data_container:
        bar_chart, pie_chart = st.columns(2)
        with bar_chart:
            dashboard_generator.generate_bar_chart("origin_amount")
        with pie_chart:
            pass#dashboard_generator.generate_pie_chart("origin_amount")
if __name__ == '__main__':
    main()