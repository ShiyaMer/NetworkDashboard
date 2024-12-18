import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import BytesIO

# Set up the Streamlit page
st.set_page_config(page_title="Network Traffic Data Visualization", layout="wide")

# Colors for consistent theming
COLORS = {
    'background': '#F3E5F5',
    'primary_purple': '#6A1B9A',
    'secondary_purple': '#9C27B0',
    'accent_purple': '#E1BEE7',
    'text_color': '#4A148C',
    'white': '#FFFFFF'
}

# Apply a global Seaborn theme
sns.set_theme(style="whitegrid")
sns.set_palette([COLORS['primary_purple'], COLORS['secondary_purple'], COLORS['accent_purple']])

# Directory for datasets
DATA_DIR = "./data"
datasets = {file.split(".")[0]: os.path.join(DATA_DIR, file) for file in os.listdir(DATA_DIR)}

# Function to load a dataset
def load_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip().str.replace(' ', '_')
        return df
    except Exception as e:
        st.error(f"[ERROR] Failed to load dataset: {file_path}, Error: {e}")
        return pd.DataFrame()

# Function to save a matplotlib figure as a downloadable file
def save_figure(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    return buffer

# Sidebar for dataset selection
st.sidebar.title("Network Traffic Data Visualization")
st.sidebar.markdown("Select a dataset and visualize network traffic patterns.")
dataset_name = st.sidebar.selectbox("Select a Dataset", list(datasets.keys()))

if dataset_name:
    df = load_dataset(datasets[dataset_name])

    if not df.empty:
        # Tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Correlation Heatmap", "Scatter Plot", "Bar Chart", "Pie Chart", "Box Plot"
        ])

        with tab1:
            st.header("Correlation Heatmap")
            numerical_df = df.select_dtypes(include=['number'])
            if not numerical_df.empty:
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.heatmap(numerical_df.corr(), annot=True, cmap="Purples", fmt=".2f", cbar=True, ax=ax)
                ax.set_title("Correlation Heatmap", fontsize=16, color=COLORS['text_color'])
                st.pyplot(fig, use_container_width=True)

                st.download_button(
                    label="Download Heatmap",
                    data=save_figure(fig),
                    file_name="correlation_heatmap.png",
                    mime="image/png"
                )
            else:
                st.warning("No numerical data available for correlation heatmap.")

        with tab2:
            st.header("Scatter Plot")
            x_feature = st.selectbox("Select X-axis feature", df.columns, key="scatter-x")
            y_feature = st.selectbox("Select Y-axis feature", df.columns, key="scatter-y")

            if x_feature and y_feature:
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.scatterplot(data=df, x=x_feature, y=y_feature, ax=ax, s=100, edgecolor='w')
                ax.set_title(f"Scatter Plot: {x_feature} vs {y_feature}", fontsize=16, color=COLORS['text_color'])
                ax.set_xlabel(x_feature, fontsize=14)
                ax.set_ylabel(y_feature, fontsize=14)
                st.pyplot(fig, use_container_width=True)

                st.download_button(
                    label="Download Scatter Plot",
                    data=save_figure(fig),
                    file_name="scatter_plot.png",
                    mime="image/png"
                )

        with tab3:
            st.header("Bar Chart")
            if 'Label' in df.columns:
                df['Label'] = df['Label'].replace({1: 'Attack', 0: 'Normal'})
                counts = df['Label'].value_counts()
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.barplot(x=counts.index, y=counts.values, ax=ax, palette="Purples")
                ax.set_title("Bar Chart", fontsize=16, color=COLORS['text_color'])
                ax.set_xlabel("Label", fontsize=14)
                ax.set_ylabel("Count", fontsize=14)
                for p in ax.patches:
                    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha='center', va='center', fontsize=12, color=COLORS['text_color'], xytext=(0, 10),
                                textcoords='offset points')
                st.pyplot(fig, use_container_width=True)

                st.download_button(
                    label="Download Bar Chart",
                    data=save_figure(fig),
                    file_name="bar_chart.png",
                    mime="image/png"
                )
            else:
                st.warning("'Label' column not found in dataset.")

        with tab4:
            st.header("Pie Chart")
            if 'Label' in df.columns:
                df['Label'] = df['Label'].replace({1: 'Attack', 0: 'Normal'})
                counts = df['Label'].value_counts()
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%', colors=sns.color_palette("Purples"), textprops={'fontsize': 12})
                ax.set_title("Pie Chart", fontsize=16, color=COLORS['text_color'])
                st.pyplot(fig, use_container_width=True)

                st.download_button(
                    label="Download Pie Chart",
                    data=save_figure(fig),
                    file_name="pie_chart.png",
                    mime="image/png"
                )
            else:
                st.warning("'Label' column not found in dataset.")

        with tab5:
            st.header("Box Plot")
            numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
            feature_col = st.selectbox("Select a feature", numerical_columns, key="box-plot-feature")

            if feature_col:
                fig, ax = plt.subplots(figsize=(12, 8))
                sns.boxplot(y=df[feature_col], ax=ax, palette="Purples", width=0.6)
                ax.set_title(f"Box Plot for {feature_col}", fontsize=16, color=COLORS['text_color'])
                ax.set_ylabel(feature_col, fontsize=14)
                st.pyplot(fig, use_container_width=True)

                st.download_button(
                    label="Download Box Plot",
                    data=save_figure(fig),
                    file_name="box_plot.png",
                    mime="image/png"
                )
    else:
        st.error("Failed to load the dataset or dataset is empty.")
else:
    st.sidebar.warning("Please select a dataset to visualize.")
