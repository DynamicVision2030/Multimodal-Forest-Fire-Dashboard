import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff

# Load datasets
train_df = pd.read_csv("train66.csv")
test_df = pd.read_csv("test66.csv")

# Set up page configuration
st.set_page_config(page_title="Comprehensive EDA for Train and Test Datasets", layout="wide")

st.title("📊 Comprehensive EDA for Train and Test Datasets")
st.markdown("This dashboard provides an interactive EDA for `train66.csv` and `test66.csv` datasets, allowing a side-by-side comparison for key metrics and visualizations.")

# Display basic info for both datasets
st.write("### Basic Information")
st.write("#### Train Dataset")
st.write(train_df.describe())
st.write("#### Test Dataset")
st.write(test_df.describe())

# Display missing values side-by-side
st.write("### Missing Values in Each Dataset")
missing_values_train = train_df.isnull().sum()
missing_values_test = test_df.isnull().sum()
missing_values_df = pd.DataFrame({
    "Train Missing Values": missing_values_train[missing_values_train > 0],
    "Test Missing Values": missing_values_test[missing_values_test > 0]
})
st.write(missing_values_df)

# Distribution plots for each numeric column
st.write("### Distribution Comparison of Features")
numeric_columns = train_df.select_dtypes(include=["float64", "int64"]).columns
for col in numeric_columns:
    fig = ff.create_distplot(
        [train_df[col].dropna(), test_df[col].dropna()],
        ["Train", "Test"], show_hist=True, show_rug=False
    )
    fig.update_layout(title_text=f"Distribution of {col}")
    st.plotly_chart(fig)

# Side-by-side correlation heatmaps for train and test datasets
st.write("### Correlation Heatmaps for Train and Test Datasets")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Train Dataset Correlation")
    corr_train = train_df.corr()
    fig_corr_train, ax_train = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_train, annot=True, cmap="coolwarm", ax=ax_train)
    st.pyplot(fig_corr_train)

with col2:
    st.subheader("Test Dataset Correlation")
    corr_test = test_df.corr()
    fig_corr_test, ax_test = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr_test, annot=True, cmap="coolwarm", ax=ax_test)
    st.pyplot(fig_corr_test)

# Side-by-side box plots for outlier detection
st.write("### Box Plot for Outlier Detection (Train vs. Test)")
selected_feature = st.selectbox("Select feature for box plot:", numeric_columns)
col1, col2 = st.columns(2)
with col1:
    fig_box_train = px.box(train_df, y=selected_feature, title=f"Train Dataset - {selected_feature}")
    st.plotly_chart(fig_box_train)
with col2:
    fig_box_test = px.box(test_df, y=selected_feature, title=f"Test Dataset - {selected_feature}")
    st.plotly_chart(fig_box_test)

# Pair plot comparison with sample data from both datasets
st.write("### Pair Plot for Feature Relationships")
st.markdown("This pair plot allows for a side-by-side comparison of feature relationships within each dataset.")
sampled_train = train_df.sample(frac=0.1, random_state=1)
sampled_test = test_df.sample(frac=0.1, random_state=1)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Train Dataset Pair Plot")
    fig_pair_train = sns.pairplot(sampled_train[numeric_columns])
    st.pyplot(fig_pair_train)

with col2:
    st.subheader("Test Dataset Pair Plot")
    fig_pair_test = sns.pairplot(sampled_test[numeric_columns])
    st.pyplot(fig_pair_test)

# Highlight correlations above a certain threshold for both datasets
st.write("### Highly Correlated Features")
correlation_threshold = st.slider("Select correlation threshold:", 0.5, 1.0, 0.7)

st.write("#### Train Dataset High Correlations")
high_corr_train = (
    corr_train.stack()
    .reset_index()
    .query("level_0 != level_1")
    .query(f"abs(0) >= {correlation_threshold}")
    .sort_values(by=0, ascending=False)
)
st.write(high_corr_train.rename(columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: "Correlation"}))

st.write("#### Test Dataset High Correlations")
high_corr_test = (
    corr_test.stack()
    .reset_index()
    .query("level_0 != level_1")
    .query(f"abs(0) >= {correlation_threshold}")
    .sort_values(by=0, ascending=False)
)
st.write(high_corr_test.rename(columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: "Correlation"}))

st.markdown("#### Note: This is a comprehensive EDA app, allowing you to explore both datasets in a visually intuitive and side-by-side manner.")
