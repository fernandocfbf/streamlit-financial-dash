import streamlit as st
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from currency_converter import CurrencyConverter

from src.constants.colors import *

class DashBoardGenerator():
    def __init__(self, title, dataloader):
        self.title = title
        self.dataloader = dataloader
        self.filtered_df = dataloader.get_card_transactions_dataframe()
        st.title(self.title)
    
    def generate_filter(self):
        today = datetime.datetime.now()
        start_date, end_date = st.date_input(
            'Select the date range',
            (datetime.date(2023, 1, 1), today),
            datetime.date(2023, 1, 1),
            today,
            format="MM.DD.YYYY")
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        self.filtered_df = self.filtered_df[(self.filtered_df['start_date'].between(start_date, end_date))]
        st.markdown(
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
        st.divider()
        
    def generate_card(self, title, value, delta, symbol='€'):
        st.markdown(
            """
            <style>
            div[data-testid="metric-container"] {
            background-color: #1d1d1d;
            padding: 1rem;
            aling-items: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.metric(label=title, value=f"{symbol} {value}", delta=delta)
        
    def generate_big_numbers(self):
        money_out = self.dataloader.get_money_out(self.filtered_df)
        currency_converter_obj = CurrencyConverter()
        money_out_real = round(currency_converter_obj.convert(money_out, 'EUR', 'BRL'), 2)
        avg_spendings = self.dataloader.get_monthly_avg_spendings()
        avg_spendings_real = round(currency_converter_obj.convert(avg_spendings, 'EUR', 'BRL'), 2)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            self.generate_card("Total Expend [EUR]", money_out, None)
        with kpi2:
            self.generate_card("Total Expend [BRL]", money_out_real, None, symbol='R$')
        with kpi3:
            self.generate_card("Avg. Spending [EUR]", avg_spendings, None)
        with kpi4:
            self.generate_card("Avg. Spending [BRL]", avg_spendings_real, None, symbol='R$')

    def generate_dataframe_chart(self):
        st.dataframe(self.filtered_df, use_container_width=True, height=500)

    def generate_raw_data(self):
        st.subheader('Raw Data')
        st.dataframe(self.filtered_df)
    
    def generate_montlhy_expenses_chart(self):
        monthly_expenses = self.filtered_df.groupby(['year', 'month', 'month_name'])["origin_amount"].sum().reset_index()
        monthly_expenses = monthly_expenses.sort_values(['year', 'month'], ascending=True)
        monthly_expenses['relative_increase'] = monthly_expenses['origin_amount'].pct_change()
        monthly_expenses['relative_increase'] = round(monthly_expenses['relative_increase'], 2)
        monthly_expenses['origin_amount'] = round(monthly_expenses['origin_amount'], 2)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_expenses['month_name'],
            y=monthly_expenses['origin_amount'],
            text=monthly_expenses['origin_amount'],
            name='Monthly Expenses'))
        fig.update_traces(
            marker_color=PRIMARY)
        fig.add_trace(go.Scatter( 
            x=monthly_expenses['month_name'], 
            y=monthly_expenses['relative_increase'], 
            text=monthly_expenses['origin_amount'], 
            line=dict(color=LIGHT_GREY, width=2, dash='dot'),
            name='Relative Increase',
            yaxis='y2'
        ))   
        fig.update_layout(
            yaxis2=dict(
                title='Relavite Increase',
                overlaying='y',
                side='right'
            ),
            yaxis= {
                'showgrid': False, # thin lines in the background
                'zeroline': False, # thick line at x=0
                'visible': False,  # numbers below
            },
            paper_bgcolor=DARK_GREY,
            plot_bgcolor=DARK_GREY,
            font_color=LIGHT_GREY,
            margin=dict(l=0, r=0, t=30, b=0),
            height=500,
            title_text='Monthly Expenses'
        )
        #fig.update_traces(mode="markers+lines")
        st.plotly_chart(fig, use_container_width=True)

    
    def generate_bar_chart(self, column, number_categories, title, height, type='total'):
        if type == 'total':
            amount_by_category = self.filtered_df.groupby('category')[column].sum().reset_index()
        elif type == 'average':
            amount_by_category = self.filtered_df.groupby(['category', 'month'])[column].sum().reset_index()
            amount_by_category = amount_by_category.groupby('category')[column].mean().reset_index()
        amount_by_category = amount_by_category.sort_values(column, ascending=True)
        amount_by_category = amount_by_category.tail(number_categories)
        amount_by_category[f"{column}_formated"] = amount_by_category[column].apply(lambda x: f"€ {round(x, 2)}")
        fig = px.bar(amount_by_category, y='category', x=column, orientation='h', text=f"{column}_formated", title=title)
        fig.update_traces(
            marker_color=PRIMARY)
        fig.update_layout(
            xaxis=dict(
                showticklabels=False,
                visible=False,
            ),
            yaxis=dict(
                showticklabels=True,
                visible=True
            ),
            xaxis_title=None,
            paper_bgcolor=DARK_GREY,
            plot_bgcolor=DARK_GREY,
            font_color=LIGHT_GREY,
            margin=dict(l=0, r=10, t=30, b=0),
            height=height
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_line_chart(self, column, categories, height):
        time_series_amount_by_category = self.filtered_df.query(f"category in {categories}")
        time_series_amount_by_category = time_series_amount_by_category.groupby(['year', 'month', 'month_name', 'category'])[column].sum().reset_index()
        time_series_amount_by_category = time_series_amount_by_category.sort_values(['year', 'month'], ascending=True)
        fig = px.line(
            time_series_amount_by_category,
            x="month_name",
            y="origin_amount",
            color='category',
            markers=True, 
            title='Time Series with Range Slider and Selectors')
        fig.update_layout(
            paper_bgcolor=DARK_GREY,
            plot_bgcolor=DARK_GREY,
            font_color=LIGHT_GREY,
            margin=dict(l=0, r=0, t=30, b=0),
            height=height
        )
        fig.update_traces(mode="markers+lines")
        st.plotly_chart(fig, use_container_width=True)
                
    def generate_pie_chart(self, column, number_categories, title, height, type='total'):
        if type == 'total':
            amount_by_category = self.filtered_df.groupby('category')[column].sum().reset_index()
        elif type == 'average':
            amount_by_category = self.filtered_df.groupby(['category', 'month'])[column].sum().reset_index()
            amount_by_category = amount_by_category.groupby('category')[column].mean().reset_index()
        amount_by_category = amount_by_category.sort_values(column, ascending=True)
        amount_by_category_to_plot = amount_by_category.tail(number_categories)
        categories = amount_by_category_to_plot['category'].to_list()
        amount_by_category_to_plot = amount_by_category_to_plot.append({
            'category': 'other',
            column: amount_by_category.query(f"category not in {categories}")[column].sum()}, 
            ignore_index=True)
        fig = go.Figure(data=[
            go.Pie(
                labels=amount_by_category_to_plot["category"],
                values=amount_by_category_to_plot[column],
                hole=.5)])
        fig.update_layout(
            title_text=title,
            paper_bgcolor=DARK_GREY,
            plot_bgcolor=DARK_GREY,
            font_color=LIGHT_GREY,
            margin=dict(l=10, r=10, t=30, b=10),
            height=height
        )
        st.plotly_chart(fig, use_container_width=True)
