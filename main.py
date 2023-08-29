from src.classes.DataGenerator import DataGenerator
from src.classes.DashBoardGenerator import DashBoardGenerator

def main():
    data_generator = DataGenerator(100)
    df = data_generator.generate_dataframe()
    dashboard_generator = DashBoardGenerator('Personal Financial Dashboard', df)
    dashboard_generator.generate_raw_data()
    dashboard_generator.generate_histogram('value')
if __name__ == '__main__':
    main()