import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

class DashBoardGenerator():
    def __init__(self, title, df):
        self.title = title
        self.df = df

        st.title(self.title)

    def generate_raw_data(self):
        st.subheader('Raw Data')
        st.write(self.df)
    
    def generate_histogram(self, column):
        st.subheader('Histogram amount')
        num_bins = st.slider(
            "Select number of bins",
            min_value=1,
            max_value=25,
            value=10 
            )
        fig, ax = plt.subplots(figsize=(8, 6))  # Set figure size
        n, bins, patches = ax.hist(self.df[column], bins=num_bins, color='skyblue', edgecolor='black')  # Set color and edgecolor

        # Set the background color to be transparent
        ax.set_facecolor('none')
        fig.patch.set_facecolor('none')

        # Customize other appearance options
        ax.grid(False)
        ax.set_xlabel('Value', color='white')
        ax.set_ylabel('Frequency', color='white')

        # Customize tick font size
        ax.tick_params(axis='both', labelsize=10, colors='grey')
        histogram_values = np.histogram(self.df[column])[0]
        st.pyplot(fig)
    

