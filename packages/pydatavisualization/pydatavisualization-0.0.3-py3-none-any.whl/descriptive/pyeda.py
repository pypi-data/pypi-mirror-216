import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot
import numpy as np
import warnings

__all__ = ["import_dataset", "read_dataset", "display_dataset_info", "display_dataset_detail", "display_summary_data",
           "display_columns", "select_numeric_variables", "select_categorical_variables",
           "visualize_distribution_of_numeric_col", "visualize_distribution_of_categorical_col", "visualize_boxplot",
           "visualize_frequency_distribution_horizontally", "visualize_frequency_distribution",
           "visualize_basic_scatter_plot", "visualize_advanced_scatter_plot", "visualize_stack_bar",
           "visualize_advanced_stack_bar", "visualize_pie_chart", "pivot_tabel", "visualize_point_plot",
           "visualize_average_bar_plot", "visualize_advanced_bar_plot", "visualize_barplot_for_categorical_col",
           "visualize_heatmap", "visualize_linear_regression", "visualize_causation", "save_data_to_csv_file",
           "visualize_time_relationship", "visualize_time_relationship_by_categorical_variable",
           "visualize_highest_percentage_datapoints", "visualize_lowest_percentage_datapoints",
           "visualize_top_ten_values", "visualize_top_highest_average"]

# --- Create List of Color Palettes ---
red_grad = ['#FF0000', '#BF0000', '#800000', '#400000', '#000000']
pink_grad = ['#8A0030', '#BA1141', '#FF5C8A', '#FF99B9', '#FFDEEB']
purple_grad = ['#4C0028', '#7F0043', '#8E004C', '#A80059', '#C10067']
color_mix = ['#F38BB2', '#FFB9CF', '#FFD7D7', '#F17881', '#E7525B', "#FFCDCD", "#FFBCBC", "#FF9090"]
black_grad = ['#100C07', 'dimgray', '#6D6A6A', '#9B9A9C', '#CAC9CD']
colors = ["lightslategrey", "crimson", "#06344d", "#b4dbe9", "royalblue"]
pastel = sns.color_palette("pastel")

#             ----------------  Libraries Settings  ---------------

pd.set_option("display.max_columns", None)
sns.set_style(style="whitegrid")
plt.rcParams["figure.dpi"] = 100
warnings.filterwarnings("ignore")

#             ----------------  EDA Methods  ---------------


def show_values(axs, orient="v", space=.01):
    def _single(axes2):
        if orient == "v":
            for p in axes2.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{:.3f}'.format(p.get_height())
                axes2.text(_x, _y, value, ha="center")
        elif orient == "h":
            for p in axes2.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.3f}'.format(p.get_width())
                axes2.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)


def import_dataset(file_name: str):
    """    
    Read cvs data file.
    
    :param file_name: string contain the csv file name
    
    :return: pandas dataframe
    
    """
    try:
        df = pd.read_csv(file_name, parse_dates=True, header=0)
        return df
    except FileNotFoundError:
        print("No such File, upload your dataset CSV file to the project")


def read_dataset(data):
    """"
    Reading data from a variable.

    :param data: variable

    :return: data

    """
    return data.head()


def display_dataset_info(data):
    """
    Print dataset info.

    :param data: variable

    :return: total rows and columns
    """
    print("\033[1m"+".: Dataset Info :."+"\033[0m")
    print("*" * 30)
    print("Total Rows: " + "\033[1m", data.shape[0])
    print("\033[0m" + "Total Columns: " + "\033[1m", data.shape[1])
    print("\033[0m" + "*" * 30)
    print("\n")


def display_dataset_detail(data):
    """
    Print dataset details.

    :param data: variable

    :return: dataset details

    """
    print("\033[1m"+".: Dataset Details :. " + "\033[0m")
    print("*" * 30)
    print(data.info(memory_usage=False))


def display_summary_data(data):
    """
    The function prints out a summary table of columns.
    
    - number of unique.
    
    - Null values.
    
    - Null Percentage.
    
    - DataType.
    
    :param data: variable
    
    :return: Summarize columns dataframe
    
    """
    summary_tabel = pd.DataFrame({"Unique": data.nunique(),
                                  "Null": data.isna().sum(),
                                  "NullPercent": data.isna().sum() / len(data),
                                  "Types": data.dtypes.values})
    print(summary_tabel)


def display_columns(data):
    """
    Separate numerical features and categorical features.
    
    :param data: variable
    
    :return: list of numerical and categorical feature names
    
    """
    numeric_variable_lst = data.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_variable_lst = data.select_dtypes(include=["object", "category"]).columns.tolist()

    print(f"Numerical Columns: {numeric_variable_lst}\nCategorical Columns: {categorical_variable_lst}")


def select_numeric_variables(data) -> list:
    """
    Selecting numerical variables.
    
    :param data: variable
    
    :return: all numeric features in a dataset
    """
    numeric_variable_lst = data.select_dtypes(exclude="object")
    return list(numeric_variable_lst)


def select_categorical_variables(data) -> list:
    """
    Selecting categorical variables.
    
    :param data: variable
    
    :return: all categorical features in a dataset
    """
    categorical_variable_lst = data.select_dtypes(include=["object", "category"])
    return list(categorical_variable_lst)


def visualize_distribution_of_numeric_col(data_frame, column_name: str, bins: int):
    """
    Visualize numerical column.

    :param data_frame: variable
    
    :param column_name: str

    :param bins: int
    
    :return: Histogram, boxplot, q-q plot, skewness and kurtosis values
    
    """
    # Testing column Type
    if not data_frame[column_name].dtype in ["int64", "float64"]:
        raise TypeError(f"{column_name} Is not a Numeric Column. Only Numeric Column is Allowed")

    print(f"\033[1m" + f".: {column_name.title()} Skewness & Kurtosis :. " + "\033[0m")
    print("*" * 40)
    print("Skewness: "+"\033[1m{:.3f}".format(data_frame[column_name].skew(axis=0, skipna=True)))
    print("\033[0m"+"Kurtosis:" + "\033[1m{:.3f}".format(data_frame[column_name].kurt(axis=0, skipna=True)))
    print("\n")

    fig = plt.figure(figsize=(10, 6))
    fig.suptitle(f"{column_name.title()} Distribution", fontweight="heavy", x=0.069, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif", color=black_grad[0])

    # Histogram
    fig.add_subplot(2, 2, 2)
    plt.title("Histogram Plot", fontweight="bold", fontsize=14, fontfamily="sans-serif", color=black_grad[1])
    sns.histplot(data=data_frame, x=column_name, kde=True, color=color_mix[0], bins=bins)
    plt.xlabel("Total", fontweight="regular", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(column_name, fontweight="regular", fontsize=11, fontfamily="sans-serif", color=black_grad[1])

    # Q-Q Plot
    ax_2 = fig.add_subplot(2, 2, 4)
    plt.title("Q-Q Plot", fontweight="bold", fontsize=14, fontfamily="sans-serif", color=black_grad[1])
    qqplot(data_frame[column_name], fit=True, line="45", ax=ax_2, markerfacecolor=color_mix[0], alpha=0.6)

    # Box Plot
    fig.add_subplot(1, 2, 1)
    sns.boxplot(data_frame, y=column_name, color=color_mix[0], boxprops=dict(alpha=0.8), linewidth=1.5)

    plt.title("Box Plot", fontweight="bold", fontsize=14, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(column_name, fontweight="regular", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_distribution_of_categorical_col(data_frame, column_name: str):
    """
    Visualize categorical column.

    :param data_frame: variable

    :param column_name: str

    :return: histogram, and pie charts

    """

    # Testing column Type
    if not data_frame[column_name].dtype in ["object", "category"]:
        raise TypeError(f"{column_name} Is a Numeric Column. Only Categorical Column is Allowed")

    print("*" * 25)
    print(f"\033[1m" + f".: {column_name.title()} Total :. " + "\033[0m")
    print("*" * 25)
    print(data_frame[column_name].value_counts(dropna=False))

    order = data_frame[column_name].value_counts().index
    fig = plt.figure(figsize=(10, 6))
    fig.suptitle(f"{column_name.title()} Distribution", fontweight="heavy", x=0.069, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0])
    # Pie Chart
    plt.subplot(1, 2, 1)
    plt.title("Pie Chart", fontweight="bold", fontsize=14, fontfamily="sans-serif", color=colors[0])
    plt.pie(data_frame[column_name].value_counts(), colors=pastel, pctdistance=0.7, autopct="%.2f%%",
            wedgeprops=dict(alpha=0.8, edgecolor=black_grad[1]), textprops={"fontsize": 12})
    centre = plt.Circle((0, 0), 0.45, fc="white", edgecolor=black_grad[1])
    plt.gcf().gca().add_artist(centre)

    # Histogram
    plt.subplot(1, 2, 2)
    plt.title("Histogram", fontweight="bold", fontsize=14, fontfamily="sans-serif", color=colors[0])
    ax = sns.countplot(x=column_name, data=data_frame, palette=pastel, order=order, edgecolor=black_grad[2],
                       alpha=0.85)
    for rect in ax.patches:
        ax.text(rect.get_x() + rect.get_width()/2, rect.get_height()+4.25, rect.get_height(),
                horizontalalignment="center", fontsize=10, bbox=dict(facecolor="none", edgecolor=black_grad[0],
                                                                     linewidth=0.25, boxstyle="round"))

    plt.xlabel(column_name.capitalize(), fontweight="bold", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel("Total", fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="y", alpha=0.4)
    plt.grid(axis="x", alpha=0)
    plt.show()


def visualize_boxplot(data_frame, numeric_column: str, categorical_column: str,
                      subtitle: str = "Explain ur data viz by subtitle"):
    """
    Visualize numeric column medians by a categorical column.

    Add new subtitle content to the third parameter.

    :param data_frame: variable

    :param numeric_column: str

    :param categorical_column: str

    :param subtitle: str

    :return: boxplot chart

    """
    if not data_frame[numeric_column].dtype in ["int64", "float64"]:
        raise TypeError(f"{numeric_column} Is not a Numeric Column. Only Numeric Column is Allowed")
    fig = plt.figure(figsize=(10, 6))
    fig.suptitle(f"Distribution of {numeric_column.title()} Grouped By {categorical_column.title()}",
                 fontweight="heavy", x=0.060, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0])
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=colors[0], loc="left", pad=12)

    medians = data_frame.groupby([categorical_column])[numeric_column].median().round(3).sort_values()

    vertical_offset = data_frame[numeric_column].median() * 0.05
    box_plot = sns.boxplot(data=data_frame, x=categorical_column, y=numeric_column,
                           medianprops={"color": "coral"}, order=medians.index, palette=color_mix[0:8])

    for xtick in box_plot.get_xticks():
        box_plot.text(xtick, medians[xtick] + vertical_offset, medians[xtick], horizontalalignment="center",
                      size=12, color=colors[1], weight="bold")

    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.xlabel(categorical_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(numeric_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.grid(axis="x", alpha=0)
    plt.grid(axis="y", alpha=0.4)
    box_plot.set(frame_on=False)
    plt.show()


def visualize_frequency_distribution_horizontally(data, first_column: str, target_column: str,
                                                  subtitle: str = "Explain ur data viz by subtitle"):
    """
    Visualize relationship of categorical variables horizontally bar.

    Add new subtitle content to the third parameter.

    :param data: variable

    :param first_column: str

    :param target_column:str

    :param subtitle:str

    :return: Horizontal bar chart

    """
    _, ax = plt.subplots(figsize=(11.5, 7))
    plt.suptitle(f"{first_column.title()} Distribution Based On {target_column.title()}",
                 fontweight="heavy", x=0.069, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=colors[0], loc="left")
    cross_tb = pd.crosstab(data[first_column], data[target_column])
    cross_tb.plot(kind="barh", color=pastel, edgecolor=colors[0], alpha=0.85,
                  ax=ax, width=0.4)
    for rect in ax.patches:
        width, height = rect.get_width(), rect.get_height()
        x, y = rect.get_xy()
        ax.text(x+width/2, y+height/2, "{:.0f}".format(width), horizontalalignment="center",
                verticalalignment="center")

    ax.legend(title=target_column.title(), bbox_to_anchor=(1, 1.08), loc="upper right", frameon=True)
    plt.grid(axis="both", alpha=0.4, lw=0.5)
    ax.set(frame_on=False)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.ylabel(first_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_frequency_distribution(data, first_column: str, target_column: str,
                                     subtitle: str = "Explain ur data viz by subtitle"):

    """
    Visualize frequency distribution of categorical variables .

    Add new subtitle content to the third parameter.


    :param data: variable

    :param first_column: str

    :param target_column: str

    :param subtitle: str

    :return: bar chart

    """
    _, ax = plt.subplots(figsize=(11, 7))
    plt.suptitle(f"{first_column.title()} Distribution Based On {target_column.title()}",
                 fontweight="heavy", x=0.030, y=0.99, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=colors[0], loc="left", pad=8)
    cross_tb = pd.crosstab(data[first_column], data[target_column])
    cross_tb.plot(kind="bar",  color=pastel, edgecolor=black_grad[2], alpha=0.85,
                  ax=ax, width=0.4)
    for rect in ax.patches:
        ax.text(rect.get_x() + rect.get_width()/2, rect.get_height()+1.25, rect.get_height(),
                horizontalalignment="center", fontsize=10)

    ax.legend(title=target_column.title(), bbox_to_anchor=(0.88, 0.90), loc="upper left", frameon=True)
    plt.grid(axis="both", alpha=0.4, lw=0.5)
    ax.set(frame_on=False)
    plt.xticks(rotation=45)
    plt.xlabel(first_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_basic_scatter_plot(data, first_column: str, second_column: str):
    """
    Visualize relationship between two numeric column.
    
    :param data: variable
    
    :param first_column: str
    
    :param second_column: str
    
    :return: Basic scatter plot
    
    """

    plt.figure(figsize=(10, 6))
    plt.suptitle(f"Relationship Between {second_column.title()} and {first_column.title()} Column",
                 fontweight="heavy", x=0.059, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title("explain ur data viz by subtitle",
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=colors[0], loc="left", pad=10)
    ax = sns.scatterplot(data=data, x=first_column, y=second_column, legend="full")

    plt.xlabel(first_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(second_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ticklabel_format(style="plain", axis="both")
    plt.grid(axis="both", alpha=0.4, lw=0.5)
    ax.set(frame_on=False)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_advanced_scatter_plot(data, first_column: str, second_column: str, by_third_column: str):
    """
    Vis the relationship between two numeric variable's by a third categorical variable,
    to dictate the color of data point's.

    :param: data: Data frame variable

    :param: first_column:str

    :param: second_column: str

    :param: by_third_column :str

    :return: Advanced scatter plot
    """
    plt.figure(figsize=(10, 6))
    plt.suptitle(f"Relationship Between {second_column.title()} per {first_column.title()} as "
                 f"{by_third_column.title()}",
                 fontweight="heavy", x=0.058, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title("explain ur data viz by subtitle",
              fontweight="heavy", fontsize=12, fontfamily="sans-serif", color=colors[0], loc="left", pad=10)

    ax = sns.scatterplot(data=data, x=first_column, y=second_column, hue=by_third_column, palette=pastel,
                         legend="full")

    plt.xlabel(first_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(second_column, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ticklabel_format(style="plain", axis="both")
    plt.grid(axis="both", alpha=0.4, lw=0.5)
    ax.legend(title=by_third_column.title(), bbox_to_anchor=(0.98, 0.90), loc="upper left", frameon=True)
    ax.set(frame_on=False)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_stack_bar(data, first_column: str, second_column: str,
                        subtitle: str = "explain ur data viz by subtitle"):
    """
    Visualize percentage relationship using two categorical variables.

    Add new subtitle content to the third parameter.

    :param: data: Data fame variable

    :param: first_column: str

    :param: second_column: str

    :param: subtitle: str

    :return: stacked bar plot

    """
    df = (data
          .groupby(first_column)[second_column]
          .value_counts(normalize=True)
          .mul(100)
          .round(2)
          .unstack())
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.suptitle(f"Percentage of {second_column.title()} by {first_column.title()}",
                 fontweight="heavy", x=0.059, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize=12, fontfamily="sans-serif", color=colors[0], loc="left", pad=15)
    # Plot
    df.plot.bar(stacked=True, color=pastel, ax=ax, width=0.4)

    # Adding bar labels
    for c in ax.containers:
        labels = [str(round(v.get_height(), 2)) + "%" if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c,
                     label_type='center',
                     labels=labels,
                     color=colors[0],
                     size=12)  # add a container object "c" as first argument
    # Removing spines
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    # Adding tick and axes labels
    ax.legend(title=second_column.title(), bbox_to_anchor=(0.98, 0.90), loc="upper left")
    ax.grid(axis="both", alpha=0.4, lw=0.5)
    ax.set(frame_on=False, xlabel=None)
    ax.tick_params(labelsize=12, labelrotation=0)
    ax.set_ylabel("Percentage", size=14, color=colors[0])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_advanced_stack_bar(data, first_column: str, second_column: str, third_column: str,
                                 subtitle: str = "explain ur data viz by subtitle"):

    """
    Visualize percentage relationship using three categorical variables.

    Add new subtitle content to the third parameter.

    :param data: variable

    :param first_column: str

    :param second_column: str

    :param third_column: str

    :param subtitle: str

    :return: stacked bar plot

    """
    df = data.groupby([first_column, second_column])[third_column].value_counts(normalize=True)\
        .mul(100).round(2).unstack()
    _, ax = plt.subplots(figsize=(11, 6))
    plt.suptitle(f"Percentage of {third_column.title()} by {first_column.title()} and {second_column.title()}",
                 fontweight="heavy", x=0.26, y=0.98,  fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=15)
    df.plot(kind="bar", stacked=True, width=0.4, ax=ax, color=pastel)

    # Adding bar labels
    for c in ax.containers:
        labels = [str(round(v.get_height(), 2)) + "%" if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c,
                     label_type='center',
                     labels=labels,
                     color=colors[0],
                     size=10)  # add a container object "c" as first argument
    # Removing spines
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    ax.legend(title=third_column.title(), bbox_to_anchor=(0.98, 0.90), loc="upper left", frameon=True)
    plt.grid(axis="both", alpha=0.4, lw=0.5)
    ax.set(frame_on=False, xlabel=None)
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_pie_chart(data, categorical_col: str, numerical_col: str,
                        subtitle: str = "explain ur data viz by subtitle"):
    """
    Visualize pie chart.

    Add new subtitle content to the third parameter.

    :param data:
    :param categorical_col:
    :param numerical_col:
    :param subtitle:
    :return: pie chart
    """
    _, ax = plt.subplots(figsize=(10, 6))
    plt.suptitle(f"Comparison {numerical_col.title()} per {categorical_col.title()}",
                 fontweight="heavy", x=0.15, y=0.99, fontsize="16", ha="left",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color="dimgray", loc="left")
    labels = data[categorical_col].unique()
    df = data.groupby(categorical_col)[numerical_col].sum()
    plt.pie(df, colors=pastel, pctdistance=0.7, autopct="%.2f%%", labels=labels,
            wedgeprops=dict(alpha=0.8, edgecolor="floralwhite"), textprops={"fontsize": 12})
    centre = plt.Circle((0, 0), 0.45, fc="white", edgecolor="aliceblue")
    plt.gcf().gca().add_artist(centre)
    ax.legend(title=categorical_col.title(), bbox_to_anchor=(1.2, 0.90), loc="upper left", frameon=True, shadow=True)

    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def pivot_tabel(data, index_col: list, columns: list, values: list, agg: str):
    """
    Create a pivot table to summarize the data.

    :param data: variable

    :param index_col: list of column name

    :param columns: list of columns name

    :param values: list of columns name

    :param agg: string of aggfunction

    :return: pivot table
    """

    pivot_table = pd.pivot_table(data, index=index_col, columns=columns, values=values, aggfunc=agg, margins=True)
    return pivot_table


def visualize_point_plot(data, numerical_col: str, categorical_col: str):
    """
    Create a point plot to visualize the mean of a numerical column
    by the categories of a categorical column.
    
    :param data: variable
    
    :param numerical_col: str
    
    :param categorical_col: str
    
    :return: point plot chart
    """
    plt.figure(figsize=(11.5, 6))
    plt.suptitle(f" Average {numerical_col.title()} per {categorical_col.title()}",
                 fontweight="heavy", x=0.050, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title("explain ur data viz by subtitle",
              fontweight="heavy", fontsize=12, fontfamily="sans-serif", color=colors[0], loc="left", pad=15)

    sns.pointplot(data, x=categorical_col, y=numerical_col, dodge=True, estimator=np.mean, ci=95, errwidth=1,
                  capsize=.1, color="k", join=False)

    # Add data labels
    mean_df = data.groupby(categorical_col)[[numerical_col]].mean()
    for i, row in enumerate(mean_df.itertuples()):
        x_value, mean = row
        plt.annotate(round(mean, 3), (i, mean), textcoords="offset points", xytext=(10, 0), ha="left")

    plt.xlabel(categorical_col, fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(f"Average {numerical_col}", fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.grid(axis="both", alpha=0.4, lw=0.5, color="grey", which="major", )
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_average_bar_plot(data, numerical_col: str, categorical_col: str):
    """
    Visualize the mean of a numerical column
    by the categories of a categorical column.

    :param data: variable

    :param numerical_col: str

    :param categorical_col: str

    :return: point plot chart
    """
    plt.figure(figsize=(10, 6))
    plt.suptitle(f" Average {numerical_col.title()} by {categorical_col.title()}",
                 fontweight="heavy", x=0.050, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title("explain ur data viz by subtitle",
              fontweight="heavy", fontsize=12, fontfamily="sans-serif", color=colors[0], loc="left", pad=15)
    order = data.groupby([categorical_col])[numerical_col].mean().round().sort_values(ascending=False).index
    ax = sns.barplot(data=data, y=categorical_col, x=numerical_col, ci=None, palette=pastel, order=order)

    show_values(ax, "h", space=0)

    plt.xlabel(f"Average", fontweight="bold", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.ylabel(f"{categorical_col}", fontweight="bold", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.grid(axis="x", alpha=0.4)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    ax.set(frame_on=False)
    plt.show()


def visualize_advanced_bar_plot(data, categorical_column: str, numerical_column: str, second_categorical_column: str,
                                subtitle: str = "Explain ur data viz by subtitle "):
    """
    Summarize two categorical columns by numerical column .

    Add new subtitle content to the third parameter.

    :param data: variable

    :param categorical_column: str

    :param numerical_column: str

    :param second_categorical_column: str

    :param subtitle: str

    :return: bar chart
    """

    _, ax = plt.subplots(figsize=(11.5, 6))
    plt.suptitle(f"The Number of {numerical_column.title()} by {categorical_column.title()} per "
                 f"{second_categorical_column.title()}", fontweight="heavy", x=0.060, y=0.990, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=colors[0], loc="left", pad=10)
    df = data.groupby([categorical_column, second_categorical_column])[numerical_column].count().reset_index()\
        .sort_values(numerical_column, ascending=False)
    ax = sns.barplot(data=df, x=numerical_column, y=categorical_column, hue=second_categorical_column, palette=pastel,
                     errwidth=0)
    for rect in ax.containers:
        ax.bar_label(rect, color=colors[0])

    ax.set(frame_on=False)

    plt.xlabel(f"{numerical_column}", labelpad=15, fontweight="bold", fontsize=16,
               fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel(f"{categorical_column}", labelpad=15, fontweight="bold", fontsize=16,
               fontfamily="sans-serif",
               color=black_grad[1])
    ax.legend(title=f"{second_categorical_column.title()}",
              bbox_to_anchor=(1.2, 1), shadow=True, title_fontsize="x-large")
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="x", alpha=0.2)
    plt.show()


def visualize_barplot_for_categorical_col(data, first_categorical_col: str, second_categorical_col: str,
                                          subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize percentage of datapoint values for categorical variable grouped by second categorical variable.

    Add new subtitle content to the third parameter.

    :param data: variable
    
    :param first_categorical_col: str
    
    :param second_categorical_col: str

    :param subtitle: str

    :return: count plot
    """
    _, ax = plt.subplots(figsize=(10, 6))
    plt.suptitle(f"Percentage of {first_categorical_col.title()} per {second_categorical_col.title()}",
                 fontweight="heavy", x=0.014, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=38)

    ax = sns.countplot(x=first_categorical_col, hue=second_categorical_col, data=data,
                       palette=pastel)

    ax.set(xlabel=first_categorical_col, frame_on=False, ylabel=None)

    for c in ax.containers:
        # custom label calculates percent and add an empty string so 0 value bars don't have a number
        labels = [f'{h / data[second_categorical_col].count() * 100:0.2f}%' if (h := v.get_height()) > 0 else '' for v
                  in c]

        ax.bar_label(c, labels=labels, label_type='edge', fontsize=12, color=black_grad[1])

    ax.legend(title=second_categorical_col.title(), bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.tight_layout()
    plt.xlabel(f"{first_categorical_col}", labelpad=10, fontweight="bold", fontsize=16,
               fontfamily="sans-serif",
               color=black_grad[1])
    plt.show()


def visualize_heatmap(data):
    """
    Visualize the correlation between multiple numeric column.
    
    :param data: variable
    
    :return: heatmap
    
    """
    numeric_features = data.select_dtypes(exclude=["object", "category"])
    plt.figure(figsize=(10, 6))
    plt.suptitle("Correlation Map",
                 fontweight="heavy", x=0.040, y=0.998, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title("explain ur data viz by subtitle",
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=10)

    sns.heatmap(numeric_features.corr(), cmap="Reds", annot=True, linewidths=0.1)

    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_linear_regression(data, numerical_column: str, numerical_col: str,
                                subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize the relationship between two numeric column.

    Add new subtitle content to the third parameter.

    :param data: variable
    
    :param numerical_column: str
    
    :param numerical_col: str

    :param subtitle: str

    :return: regression plot
    """
    corr = data[numerical_column].corr(data[numerical_col])
    print("*" * 25)
    print("Correlation between ", numerical_column.title(), " and ", numerical_col.title(), " is ",
          round(corr, 2))
    print("*" * 25)
    _, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x=numerical_column, y=numerical_col, data=data, line_kws={"color": "red"}, ax=ax)

    plt.suptitle(f"Correlation Between {numerical_column.title()} and {numerical_col.title()}",
                 fontweight="heavy", x=0.058, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="10", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=38)
    plt.xlabel(numerical_column.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel(numerical_col.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="x", alpha=0)
    plt.grid(axis="y", alpha=0.4)
    plt.show()


def visualize_causation(data, numerical_column: str, numerical_col: str, categorical: str,
                        subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize the relationship between two numeric column by a categorical column.

    Add new subtitle content to the third parameter.

    :param data: variable

    :param numerical_column: str

    :param numerical_col: str

    :param categorical: str

    :param subtitle:str

    :return: regression plot
    """

    sns.lmplot(x=numerical_column, y=numerical_col, hue=categorical, data=data, palette=pastel, legend=False, height=6,
               aspect=1.5)
    plt.suptitle(f"Correlation Between {numerical_column.title()} and {numerical_col.title()}",
                 fontweight="heavy", x=0.065, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="10", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=40)
    plt.xlabel(numerical_column.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel(numerical_col.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif", color=black_grad[1])
    plt.legend(title=categorical.title(), bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="x", alpha=0)
    plt.grid(axis="y", alpha=0.4)
    plt.show()


def save_data_to_csv_file(data, filename: str):
    """
    Save data to a csv file.

    :param data: variable

    :param filename: string

    :return: updated csv data file
    """
    new_data = data.to_csv(filename, index=False)
    return new_data


def visualize_time_relationship(data, date_colum: str, numerical_column: str, filter_by: str,
                                subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize the sum of all shared data points for continuous variable by date variable, filter by :

    - Year

    - Month

    - Day

    :param data:
    :param date_colum:
    :param numerical_column:
    :param filter_by:
    :param subtitle:
    :return: Line Chart
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    if filter_by.lower() == "month":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.month
        sns.lineplot(data=data, x=filter_by, y=numerical_column, linewidth=1, estimator="sum", errorbar=None, ax=ax)
    elif filter_by.lower() == "year":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.year
        sns.lineplot(data=data, x=filter_by, y=numerical_column, linewidth=1, estimator="sum", errorbar=None, ax=ax)
    elif filter_by.lower() == "day":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.day
        sns.lineplot(data=data, x=filter_by, y=numerical_column, linewidth=1, estimator="sum", errorbar=None, ax=ax)
    plt.suptitle(f"{numerical_column.title()} Relationship by {filter_by.title()}",
                 fontweight="heavy", x=0.065, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="10", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=20)
    plt.xlabel(filter_by.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel(numerical_column.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="x", alpha=0)
    plt.grid(axis="y", alpha=0.4)
    ax.locator_params(integer=True)
    plt.show()


def visualize_time_relationship_by_categorical_variable(data, date_colum: str, numerical_col: str,
                                                        categorical_colum, filter_by: str,
                                                        subtitle: str = "explain ur data viz by subtitle "):
    """
        Visualize the sum between date column and continues column with categorical column, filter by :

        - Year

        - Month

        - Day

        :param data:
        :param date_colum:
        :param numerical_col:
        :param filter_by:
        :param categorical_colum:
        :param subtitle:
        :return: Line Chart
        """
    fig, ax = plt.subplots(figsize=(10, 6))
    if filter_by.lower() == "month":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.month
        sns.lineplot(data=data, x=filter_by, y=numerical_col, hue=categorical_colum, linewidth=2, estimator="sum",
                     errorbar=None, color=pastel, ax=ax)
    elif filter_by.lower() == "year":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.year
        sns.lineplot(data=data, x=filter_by, y=numerical_col, hue=categorical_colum,
                     linewidth=2, estimator="sum", color=pastel, errorbar=None, ax=ax)
    elif filter_by.lower() == "day":
        data[date_colum] = pd.to_datetime(data[date_colum])
        data[filter_by] = data[date_colum].dt.day
        sns.lineplot(data=data, x=filter_by, y=numerical_col, hue=categorical_colum,
                     linewidth=2, estimator="sum", color=pastel, errorbar=None, ax=ax)

    plt.suptitle(f"{categorical_colum.title()} Relationship by {numerical_col.title()} per {filter_by.title()}",
                 fontweight="heavy", x=0.065, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="10", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=20)
    plt.xlabel(filter_by.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.ylabel(numerical_col.upper(), fontweight="regular", fontsize=11, fontfamily="sans-serif",
               color=black_grad[1])
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.grid(axis="x", alpha=0)
    plt.grid(axis="y", alpha=0.4)
    ax.locator_params(integer=True)
    plt.legend(title=categorical_colum.title(), bbox_to_anchor=(1, 1.02), loc="upper left", shadow=True)
    plt.tight_layout(rect=[0, 0.04, 1, 1.025])
    plt.show()


def visualize_highest_percentage_datapoints(data, first_categorical_col: str, second_categorical_col: str,
                                            subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize the highest percentage of datapoint values,

    for categorical variable grouped by second categorical variable.

    Add new subtitle content to the third parameter.

    :param data: variable

    :param first_categorical_col: str

    :param second_categorical_col: str

    :param subtitle: str

    :return: count plot
    """
    _, ax = plt.subplots(figsize=(10, 6))
    plt.suptitle(f"{first_categorical_col.title()} Highest Percentage per {second_categorical_col.title()}",
                 fontweight="heavy", x=0.044, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=40)

    ax = sns.countplot(x=first_categorical_col, hue=second_categorical_col, data=data,
                       color="aquamarine", saturation=0.5)

    ax.set(xlabel=first_categorical_col, frame_on=False, ylabel=None)

    for c in ax.containers:
        # custom label calculates percent and add an empty string so 0 value bars don't have a number
        labels = [f'{h / data[second_categorical_col].count() * 100:0.1f}%' if (h := v.get_height()) > 0 else '' for v
                  in c]

        ax.bar_label(c, labels=labels, label_type='edge', fontsize=12, color=black_grad[1])

    # highest value
    patch_h = [patch.get_height() for patch in ax.patches]
    idx_tallest = np.argmax(patch_h)
    ax.patches[idx_tallest].set_facecolor("slateblue")

    ax.legend(title=second_categorical_col.title(), bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.tight_layout()
    plt.xlabel(f"{first_categorical_col}", labelpad=10, fontweight="bold", fontsize=16,
               fontfamily="sans-serif",
               color=black_grad[1])
    plt.show()


def visualize_lowest_percentage_datapoints(data, first_categorical_col: str, second_categorical_col: str,
                                           subtitle: str = "explain ur data viz by subtitle "):
    """
    Visualize the lowest percentage of datapoint values,

    for categorical variable grouped by second categorical variable.

    Add new subtitle content to the third parameter.

    :param data: variable

    :param first_categorical_col: str

    :param second_categorical_col: str

    :param subtitle: str

    :return: count plot
    """
    _, ax = plt.subplots(figsize=(10, 6))
    plt.suptitle(f"{first_categorical_col.title()} Lowest Percentage per {second_categorical_col.title()}",
                 fontweight="heavy", x=0.044, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle.capitalize(),
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=40)

    ax = sns.countplot(x=first_categorical_col, hue=second_categorical_col, data=data,
                       color="aquamarine", saturation=0.5)

    for c in ax.containers:
        # custom label calculates percent and add an empty string so 0 value bars don't have a number
        labels = [f'{h / data[second_categorical_col].count() * 100:0.1f}%' if (h := v.get_height()) > 0 else '' for v
                  in c]
        ax.bar_label(c, labels=labels, label_type='edge', fontsize=10, color=colors[0])

    # Lowest value
    patch_h = [patch.get_height() for patch in ax.patches]
    idx_tallest = np.argmin(patch_h)
    ax.patches[idx_tallest].set_facecolor("tomato")

    ax.set(xlabel=first_categorical_col, frame_on=False, ylabel=None)
    ax.legend(title=second_categorical_col.title(), bbox_to_anchor=(1, 1.02), loc="upper left")
    plt.tight_layout()
    plt.xlabel(f"{first_categorical_col}", labelpad=10, fontweight="bold", fontsize=16,
               fontfamily="sans-serif",
               color=black_grad[1])
    plt.show()


def visualize_top_ten_values(data_frame, first_column: str, second_column: str, limit_number: int,
                             subtitle: str = "Explain ur data viz by subtitle "):
    """
    Visualize the top 10  values from two  categorical columns limit the number to determine which bars to color.

    Add new subtitle content to the third parameter.

    :param data_frame: variable

    :param second_column: str

    :param first_column: str

    :param limit_number: int

    :param subtitle: str

    :return: bar chart
    """

    _, ax = plt.subplots(figsize=(10, 6))

    grouped_data = data_frame.groupby(first_column)[second_column].count().sort_values(ascending=False).head(10)

    plt.suptitle(f"{first_column.title()} with the most {second_column.title()} ",
                 fontweight="heavy", x=0.069, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=10)

    set_colors = [colors[0] if x < limit_number else colors[1] for x in grouped_data.values]
    fig = sns.barplot(data=pd.DataFrame(grouped_data).transpose(), orient="h", palette=set_colors)
    fig.set_ylabel(first_column, fontsize=12)
    fig.set_xlabel(f"\nCount of {second_column.title()}", fontsize=12)
    fig.set_yticklabels(fig.get_yticklabels(), rotation=0)

    for p in fig.patches:
        width = p.get_width()
        if width < limit_number:
            clr = colors[2]
        else:
            clr = colors[3]
        plt.text(-30 + p.get_width(), p.get_y()+0.45*p.get_height(), "{:.0f}".format(width), color=clr,
                 ha="center", va="center", fontsize="large")
    sns.despine(right=True, top=True, left=True)
    plt.tight_layout()
    plt.show()


def visualize_top_highest_average(data_frame, categorical_column: str, numerical_column: str, avg_numbers: list,
                                  subtitle: str = "Explain ur data viz by subtitle "):
    """
    Visualize the highest average values.

    add avg_numbers to determine which bars to be colored.

    Add new subtitle content to the third parameter.

    :param data_frame:
    :param categorical_column:
    :param numerical_column:
    :param avg_numbers:
    :param subtitle:
    :return: bar chart
    """

    df_cat = data_frame.loc[data_frame[categorical_column].isin(data_frame[categorical_column].value_counts().head(10)
                                                                .index)]

    numer = df_cat.groupby(categorical_column)[numerical_column].mean().round(3)\
        .astype("float64").sort_values(ascending=False)
    _, ax = plt.subplots(figsize=(10, 6))
    plt.suptitle(f"Average {numerical_column.title()} per {categorical_column.title()} ",
                 fontweight="heavy", x=0.069, y=0.98, ha="left", fontsize="16",
                 fontfamily="sans-serif",
                 color=black_grad[0]
                 )
    plt.title(subtitle,
              fontweight="heavy", fontsize="12", fontfamily="sans-serif", color=black_grad[1], loc="left", pad=15)

    set_colors = [colors[1] if x in avg_numbers else colors[0] for x in numer.values]
    fig = sns.barplot(data=pd.DataFrame(numer).transpose(), orient="h", palette=set_colors)
    fig.set_ylabel(categorical_column, fontsize=12)
    fig.set_xlabel(f"\nMean {numerical_column.title()}", fontsize=12)
    fig.set_yticklabels(fig.get_yticklabels(), rotation=0)

    for p in fig.patches:
        width = p.get_width()
        if width in avg_numbers:
            clr = colors[2]
        else:
            clr = colors[3]
        plt.text(-25 + p.get_width(), p.get_y() + 0.50 * p.get_height(), "{:.0f}".format(width), color=clr,
                 ha="center", va="center", fontsize="medium")
    sns.despine(right=True, top=True, left=True)
    show_values(fig, "h")
    plt.tight_layout()
    plt.show()
