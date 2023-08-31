import streamlit as st
import datetime
import matplotlib.pyplot as plt

from src.constants.colors import *

class DashBoardGenerator():
    def __init__(self, title, df):
        self.title = title
        self.original_df = df
        self.filtered_df = df.copy()
        st.title(self.title)
    
    def generate_side_bar(self):
        today = datetime.datetime.now()
        start_date, end_date = st.sidebar.date_input(
            'Select the date range',
            (datetime.date(2023, 1, 1), today),
            datetime.date(2023, 1, 1),
            today,
            format="MM.DD.YYYY")
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        self.filtered_df = self.filtered_df[(self.filtered_df['start_date'].between(start_date, end_date))]
        st.sidebar.markdown(
            """
            <style>
            div[data-testid="stDateInput"] {
            background-color: #34355B;
            padding: 1rem;
            aling-items: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.sidebar.subheader('Category')

        category_list = self.original_df['category'].unique()
        category_list.sort()
        val = [None]* len(category_list)
        for i, cat in enumerate(category_list):
            val[i] = st.sidebar.checkbox(cat, value=True) 
        self.filtered_df = self.original_df[self.original_df.category.isin(category_list[val])].reset_index(drop=True)

    def generate_card(self, title, value, delta):
        st.markdown(
            """
            <style>
            div[data-testid="metric-container"] {
            background-color: #34355B;
            padding: 1rem;
            aling-items: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.metric(label=title, value=f"€ {value}", delta=delta)

    def generate_raw_data(self):
        st.subheader('Raw Data')
        st.dataframe(self.filtered_df)
    
    def generate_bar_chart(self, column, title, height, type='total'):
        if title:
            st.subheader(title)
        if type == 'total':
            amount_by_category = self.filtered_df.groupby('category')[column].sum().reset_index()
        elif type == 'average':
            amount_by_category = self.filtered_df.groupby(['category', 'month'])[column].sum().reset_index()
            amount_by_category = amount_by_category.groupby('category')[column].mean().reset_index()
        amount_by_category = amount_by_category.sort_values(column, ascending=True)
        fig, ax = plt.subplots()
        fig.set_figheight(height)
        bars = ax.barh(amount_by_category['category'], amount_by_category[column],color=ACCENT_GREEN, )
        for bar in bars:
            value = bar.get_width()
            formated_value = f"€ {round(value)}"
            ax.text(value + (value*0.02), bar.get_y() + bar.get_height()/2, formated_value, va='center', color=LIGHT_GREY, fontsize=12)
        ax.tick_params(axis='y', colors=LIGHT_GREY, labelsize=12)
        ax.axes.get_xaxis().set_visible(False)
        ax.set_facecolor('none')
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        fig.patch.set_facecolor(DARK_GREY)
        st.pyplot(plt)
    
    def generate_line_chart(self, column, title, height):
        st.subheader(title)
        time_series_amount_by_category = self.filtered_df.groupby(['year', 'month', 'month_name', 'category'])[column].sum().reset_index()
        time_series_amount_by_category = time_series_amount_by_category.sort_values(['year', 'month'], ascending=True)
        fig, ax = plt.subplots()
        fig.set_figheight(height)
        for category in time_series_amount_by_category['category'].unique():
            category_df = time_series_amount_by_category[time_series_amount_by_category['category'] == category]
            ax.plot(category_df['month_name'], category_df[column], label=category, marker='o', markersize=2, linestyle='--', linewidth=1)
        ax.set_facecolor('none')
        fig.patch.set_facecolor(DARK_GREY)
        ax.grid(axis='y', color=LIGHT_GREY, alpha=0.3)
        ax.tick_params(axis='x', colors=LIGHT_GREY)
        ax.tick_params(axis='y', colors=LIGHT_GREY)
        plt.xticks(rotation=35, fontsize=5)
        plt.yticks(fontsize=5)
        ax.legend(bbox_to_anchor=(0., -0.6, 1, 0.1), loc='lower left', ncol=4, mode="expand", fontsize=5, frameon=False)
        for text in ax.get_legend().get_texts():
            text.set_color(LIGHT_GREY)
        for spine in ax.spines:
            ax.spines[spine].set_visible(False)
        st.pyplot(plt)
                
    def generate_pie_chart(self, column, title, height, type='total'):
        if title:
            st.subheader(title)
        if type == 'total':
            amount_by_category = self.filtered_df.groupby('category')[column].sum().reset_index()
        elif type == 'average':
            amount_by_category = self.filtered_df.groupby(['category', 'month'])[column].sum().reset_index()
            amount_by_category = amount_by_category.groupby('category')[column].mean().reset_index()
        fig, ax = plt.subplots()
        fig.set_figheight(height)
        ax.pie(
            amount_by_category[column],
            labels=amount_by_category['category'],
            autopct='%1.1f%%',
            shadow=False,
            startangle=90,
            textprops={'color':LIGHT_GREY, 'fontsize': 8},
            pctdistance=0.85,
            explode=[0.05]*len(amount_by_category),
            colors=GRADIENT_FOR_PIE)
        my_circle=plt.Circle( (0,0), 0.7, color=DARK_GREY)
        p=plt.gcf()
        p.gca().add_artist(my_circle)
        ax.axis('equal')
        ax.set_facecolor('none')
        fig.patch.set_facecolor(DARK_GREY)
        st.pyplot(plt)
