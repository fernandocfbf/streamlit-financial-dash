import streamlit as st
import matplotlib.pyplot as plt

from src.constants.colors import *

class DashBoardGenerator():
    def __init__(self, title, df):
        self.title = title
        self.original_df = df
        self.filtered_df = df.copy()
        st.title(self.title)
    
    def generate_side_bar(self):
        st.sidebar.write("## Filters")
        category_list = self.original_df['category'].unique()
        category_list.sort()
        val = [None]* len(category_list)
        for i, cat in enumerate(category_list):
            val[i] = st.sidebar.checkbox(cat, value=True) 
        self.filtered_df = self.original_df[self.original_df.category.isin(category_list[val])].reset_index(drop=True)

    def generate_card(self, title, value, delta):
        st.metric(label=title, value=f"€ {value}", delta=delta)

    def generate_raw_data(self):
        st.subheader('Raw Data')
        st.dataframe(self.filtered_df)
    
    def generate_bar_chart(self, column):
        st.subheader('Amount by category')
        amount_by_category = self.filtered_df.groupby('category')[column].sum()
        fig, ax = plt.subplots()
        bars = ax.bar(amount_by_category.index, amount_by_category.values, color=ACCENT_GREEN)
        for bar in bars:
            yval = bar.get_height()
            yval_formated = f"€ {yval:,.2f}"
            ax.text(bar.get_x() + bar.get_width()/2, yval + 50, yval_formated, ha='center', va='bottom', fontsize=8, color=LIGHT_GREY)
        plt.gca().axes.get_yaxis().set_visible(False)
        ax.tick_params(axis='x', colors=LIGHT_GREY)
        plt.xticks(rotation=35, fontsize=8)
        ax.set_facecolor('none')
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        fig.patch.set_facecolor(DARK_GREY)
        st.pyplot(plt)

    def generate_pie_chart(self, column):
        st.subheader('Percentage by category')
        amount_by_category = self.filtered_df.groupby('category')[column].sum().reset_index()
        fig, ax = plt.subplots()
        ax.pie(amount_by_category[column], labels=amount_by_category['category'], autopct='%1.1f%%', shadow=False, startangle=90)
        plt.gca().axes.get_yaxis().set_visible(False)
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')
        st.pyplot(plt)
