import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import itertools
from sklearn.cluster import OPTICS, DBSCAN, KMeans
from matplotlib import cm
from lifelines import KaplanMeierFitter
import math
from scipy import stats


def cluster_3d(df, cols, c_type='k-means', number=None, min_sample=3, eps=0.5,
               lab1=None, lab2=None, lab3=None, legend=False, path=None, name='cluster3d'):
    """
    Plots a three-dimensional graph of clusters for the three specified numerical columns.
    The type of clustering as well as some minor fine-tuning of clustering model
    are available.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset that contains the feature that will be plotted.
        cols : list, mandatory
            A list with three element of type str which are the column names.
        c_type : str, optional
            The type of clustering model. The available options are DBSCAN, OPTICS
            and k-means. If no type is specified, k-means will be preformed.
        number : int, optional
            The number of clusters. This parameter is only used for k-means. The
            default value is the smallest number of clusters with an inertia value
            less than 50.
        min_sample : int, optional
            The minimum number of samples in a cluster. This parameter is only used
            for DBSCAN and OPTICS. The default value is 3.
        eps: float, optional
            The maximum distance between samples for them to fall into the same cluster.
            This parameter is only used for DBSCAN. The default value is 0.5.
        lab1 : str, optional
            The label for axis 1. The default option is the name of the column in
            the data frame.
        lab2 : str, optional
            The label for axis 2. The default option is the name of the column in
            the data frame.
        lab3 : str, optional
            The label for axis 3. The default option is the name of the column in
            the data frame.
        legend : bool, optional
            Show legend or not. default is False.
        path : str, optional
            The directory path to save the plot in. Plot will not be saved if not specified.
        name : str, optional
            Name of the plot. The default is cluster3d.

        Returns
        -------
        fig : plt.figure
        ax : axes.Axes
        The figure and axes of the plot.

        Example
        --------
        > cluster_3d(df = data, cols = ['age','height','BMI'], c_type = "DBSCAN", lab1 = "Age",
        lab2 = "Height")
    """
    c_type = c_type.lower()
    if len(cols) != 3:
        return 'Wrong number of columns'
    if c_type == 'optics':
        clusters = OPTICS(min_samples=min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    elif c_type == 'dbscan':
        clusters = DBSCAN(eps=eps, min_samples=min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    else:
        if number is None:
            number = 15
            for k in range(1, 15):
                clusters = KMeans(n_clusters=k).fit(df[cols])
                if clusters.inertia_ < 50:
                    number = k
                    break
            clusters = KMeans(n_clusters=number).fit(df[cols])
            df['Clusters'] = clusters.labels_

    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(cols[0])
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(cols[1])
    if not (lab3 is None) and type(lab3) == str:
        ax.set_zlabel(lab3)
    else:
        ax.set_zlabel(cols[2])

    for s in df.Clusters.unique():
        ax.scatter(df[cols[0]].loc[df.Clusters == s], df[cols[1]].loc[df.Clusters == s], 
                   df[cols[2]].loc[df.Clusters == s], label=s)
    if legend:
        ax.legend(loc='upper left')
    if path is not None:
        fig.savefig(f'{path}/{name}.png', format='png', bbox_inches='tight')
    return fig, ax


def cluster_2d(df, cols, c_type='k-means', number=None, min_sample=3, eps=0.5,
               lab1=None, lab2=None, path=None, name='cluster2d'):
    """
    Plots a two-dimensional graph of clusters for the two specified numercial columns.
    The type of clustering as well as some minor fine-tuning of clustering model
    are available.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset that contains the feature that will be plotted.
        cols : list, mandatory
            A list with two element of type str which are the column names.
        c_type : str, optional
            The type of clustering model. The available options are DBSCAN, OPTICS
            and k-means. If no type is specified, k-means will be preformed.
        number : int, optional
            The number of clusters. This parameter is only used for k-means. The
            default value is the smallest number of clusters with an inertia value
            less than 50.
        min_sample : int, optional
            The minimum number of samples in a cluster. This parameter is only used
            for DBSCAN and OPTICS. The default value is 3.
        eps: float, optional
            The maximum distance between samples for them to fall into the same cluster.
            This parameter is only used for DBSCAN. The default value is 0.5.
        lab1 : str, optional
            The label for axis 1. The default option is the name of the column in
            the data frame.
        lab2 : str, optional
            The label for axis 2. The default option is the name of the column in
            the data frame.
        path : str, optional
            The directory path to save the plot in. Plot will not be saved if not specified.
        name : str, optional
            Name of the plot. The default is cluster2d.

        Returns
        -------
        fig : plt.figure
        ax : axes.Axes
        The figure and axes of the plot.

        Example
        --------
        > cluster_2d(df = data, cols = ['age','height'], c_type = "OPTICS", lab1 = "Age",
        lab2 = "Height")
    """
    c_type = c_type.lower()
    if len(cols) != 2:
        return 'Wrong number of columns'
    if c_type == 'optics':
        clusters = OPTICS(min_samples=min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    elif c_type == 'dbscan':
        clusters = DBSCAN(eps=eps, min_samples=min_sample).fit(df[cols])
        df['Clusters'] = clusters.labels_
    else:
        if number is None:
            number = 15
            for k in range(1, 15):
                clusters = KMeans(n_clusters=k).fit(df[cols])
                if clusters.inertia_ < 50:
                    number = k
                    break
        clusters = KMeans(n_clusters=number).fit(df[cols])
        df['Clusters'] = clusters.labels_

    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = sns.scatterplot(data=df, x=cols[0], y=cols[1], hue=df['Clusters'])

    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(cols[0])
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(cols[1])
    if path is not None:
        fig.savefig(f'{path}/{name}.png', format='png', bbox_inches='tight')

    return fig, ax


def graph_3d(df, ax1: str, ax2: str, ax3: str, lab1=None, lab2=None, lab3=None,
             path=None, name="graph3d"):
    """
    Plots a three-dimensional graph based on the three columns entered.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset that contains the feature that will be plotted.
        ax1 : str, mandatory
            The name of the column for axis 1 containing the feature to be plotted.
        ax2 : str, mandatory
            The name of the column for axis 2 containing the feature to be plotted.
        ax3 : str, mandatory
            The name of the column for axis 3 containing the feature to be plotted.
        lab1 : str, optional
            The label for axis 1. The default option is the name of the column in
            the data frame.
        lab2 : str, optional
            The label for axis 2. The default option is the name of the column in
            the data frame.
        lab3 : str, optional
            The label for axis 3. The default option is the name of the column in
            the data frame.
        path : str, optional
            The directory path to save the plot in. Plot will not be saved if not specified.
        name : str, optional
            Name of the plot. The default is graph3d.
        

        Returns
        -------
        fig : plt.figure
        ax : axes.Axes
        The figure and axes of the plot.

        Example
        --------
        > graph_3d(df = health_data, ax1 = "sbp", ax2 = "dbp", ax3 = "chd", lab1 = "SBP",
        lab2 = "DBP", lab3 = "CHD")
    """
    sns.set(style="whitegrid")
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')
    if not (lab1 is None) and type(lab1) == str:
        ax.set_xlabel(lab1)
    else:
        ax.set_xlabel(ax1)
    if not (lab2 is None) and type(lab2) == str:
        ax.set_ylabel(lab2)
    else:
        ax.set_ylabel(ax2)
    if not (lab3 is None) and type(lab3) == str:
        ax.set_zlabel(lab3)
    else:
        ax.set_zlabel(ax3)
    ax.scatter(df[ax1], df[ax2], df[ax3], color='purple')
    if path is not None:
        fig.savefig(f'{path}/{name}.png', format='png', bbox_inches='tight')
    plt.show()
    return fig, ax


def f_test(group1, group2):
    """
    Return the p-value given two groups' data.

            Parameters
            ----------
            group1 : series or list, mandatory
                Containing continuous numbers for F-test from group 1.
            group2 : series or list, mandatory
                Containing continuous numbers for F-test from group 2.

            Returns
            -------
            p_value : float
                A number round to 3 decimal places.

            Examples
            --------
            > a = [0.28, 0.2, 0.26, 0.28, 0.5]
            > b = [0.2, 0.23, 0.26, 0.21, 0.23]
            > f_test(a, b)
            0.004
    """
    x = np.array(group1)
    y = np.array(group2)
    if np.var(group2, ddof=1) != 0:
        f_value = np.var(group1, ddof=1) / np.var(group2, ddof=1)
        nun = x.size - 1
        dun = y.size - 1
        p_value = round(1 - stats.f.cdf(f_value, nun, dun), 3)
    else:
        p_value = np.nan
    return p_value


def demo_graph(var: list, input_data: pd.DataFrame, group=None):
    """
    Show the count of categorical characteristic variables in each group and combine with a summary table.
    Show the boxplot of countinous characteristic variables in each group and combine with a smmary table.

        Parameters
        ----------
        var : list, mandatory
            List of the characteristic variables. The list can include both categorical and countinous variables.
            The function can automatically detect its type and then use proper plot.
        input_data : pd.DataFrame, mandatory
            Input dataset name.
        group : names of variables in input_data, optional
            Grouping variables that will produce plottings and summary tables with different colors
            (e.g. treatment group).

        Returns
        -------
        tuple (fig_list, ax_list) : list of Figure, list of axes.Axes
        The matplotlib figures and axes containing the plots and summary tables.

        See Also
        --------
        longitudinal_graph

        Examples
        --------
        > demo_graph(var=['gender','age'], input_data=data, group="treatment")

    """
    fig_list = []
    ax_list = []
    # iterate through different variables
    for col in var:
        # set up figure, axes
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        # sort dataset
        if group is not None:
            dat = input_data.sort_values(by=[group, col], ascending=True)
        else:
            dat = input_data.sort_values(by=[col], ascending=True)
        # check the type of variable (if numeric)
        if np.issubdtype(input_data[col].dtype, np.number):
            # generate boxplot
            sns.boxplot(ax=ax, data=dat, y=col, x=group, orient="v")
            # generate summary table (descriptive statistic for numeric variables)
            if group is not None:
                summary = dat.groupby([group])[col].describe(percentiles=[0.5]).round(2).transpose()
            else:
                summary = dat[col].describe(percentiles=[0.5]).round(2).reset_index().set_index('index')
        # check the type of variable (if categorical)
        else:
            summary = pd.DataFrame()
            # generate count plot
            # generate summary table (percentage for categorical variables)
            if group is not None:
                sns.countplot(ax=ax, data=dat, x=group, hue=col)
                summary['result'] = dat.groupby([group])[col].value_counts().astype(str) + " (" \
                    + round(dat.groupby([group])[col].value_counts(normalize=True) * 100, 2).astype(str) + "%)"
                summary = summary.reset_index()
                summary = summary.pivot(index=col, columns=group)
                plt.legend(loc='upper left')
            else:
                sns.countplot(ax=ax, data=dat, x=col, hue=col, dodge=False)
                plt.xticks([], [])
                summary['result'] = dat[col].value_counts().astype(str) + \
                    " (" + round(dat[col].value_counts(normalize=True) * 100, 2).astype(str) + "%)"
        ax.set(xlabel=None)
        # combine summary table with plot
        plt.table(cellText=summary.values, rowLabels=[" ".join(i.split()[:3]) for i in summary.index],
                  loc='bottom', bbox=[0, -0.3, 1, 0.2], cellLoc="center")
        # format adjust
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.ylabel(col, fontsize=16)
        plt.title(f"Plot and summary table for {col.title()}", fontsize=30)
        # append multiple plots into list
        fig_list.append(fig)
        ax_list.append(ax)

    return fig_list, ax_list


def longitudinal_graph(outcome: list, time, group, input_data: pd.DataFrame):
    """
    Show the scatter plot of outcome means over time in each group and combine with a summary table. Function for
    longitudinal data analysis.

        Parameters
        ----------
        outcome : list, mandatory
            List of the continuous outcome(y) variables need to be plotted.
        time : names of variables in input_data, mandatory
            Time variables(x)(e.g. visit number).
        group : names of time variables in input_data, mandatory
            Grouping variables that will produce plottings and summary tables with different colors
            (e.g. treatment group).
        input_data : pd.DataFrame, mandatory
            Input dataset name.

        Returns
        -------
        tuple (fig_list, ax_list) : list of Figure, list of axes.Axes
        The matplotlib figures and axes containing the plots and summary tables.

        See Also
        --------
        demo_graph

        Examples
        --------
        > longitudinal_graph(outcome=["change_from_baseline"], time="visit", group="treatment", input_data=data)

    """
    fig_list = []
    ax_list = []
    # get unique time point
    time_uni = input_data[time].unique()
    # get unique group name
    group_uni = input_data[group].unique()
    # iterate through different outcome variables
    for col in outcome:
        # generate summary table for mean value in each group
        summary = round(input_data.groupby(by=[group, time])[col].mean().reset_index(), 2)
        # set up figure, ax
        fig, ax = plt.subplots(figsize=(15, 9))
        ax.tick_params(axis='both', which='major', labelsize=20)
        sns.set_theme(font_scale=1.2, palette="Set2")
        # generate line plot
        sns.lineplot(x=time, y=col, hue=group, data=summary)

        temp = pd.DataFrame()
        # performing F-test between every two of the groups
        for i in time_uni:
            for g1, g2 in itertools.combinations(range(len(group_uni)), 2):
                a = input_data.query(f"{time}=={i} and {group}=='{group_uni[g1]}'")[col].transpose()
                b = input_data.query(f"{time}=={i} and {group}=='{group_uni[g2]}'")[col].transpose()
                p_value = f_test(a, b)
                row = pd.DataFrame([[i, f"p-value: \n {group_uni[g1]} vs {group_uni[g2]}", p_value]],
                                   columns=["Time", "Compare", col])
                temp = pd.concat([temp, row])
        temp = temp.pivot_table(index='Compare', columns="Time")
        summary = summary.pivot_table(index=group, columns=time)
        summary = pd.concat([summary, temp])

        # combine summary table with line plot
        plt.table(cellText=summary.values, rowLabels=summary.index, loc='bottom', bbox=[0, -0.5, 1, 0.4],
                  cellLoc="center")
        # format adjust
        ax.set(xlabel=None)
        plt.subplots_adjust(left=0.2, bottom=0.3)
        plt.title(f"Line plot and summary table for {col.title()}", fontsize=30)
        # append multiple plots into list
        fig_list.append(fig)
        ax_list.append(ax)
    return fig_list, ax_list


def relation(df, gtype=3, path=None, name_chi='chiheatmap', name_cor='corheatmap'):
    """
    Plots a heat-map of the relationship between features of the same type. If type of feature
    (numerical or categorical) is not specified, both heat-maps will be drawn. The measure used
    is chi-squared for categorical and correlation for numerical types. This function does not
    calculate the relationship between categorical and numerical values.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset.
        gtype : int, optional
            Type of feature. 1 for categorical (chi-squared), 2 for numerical (correlation)
            any other number for both. The default is 3 (both).
        path : str, optional
            The directory path to save the plot in. Plot will not be saved if not specified.
        name_chi : str, optional
            Name of the plot for the categorical features. The default is chiheatmap.
        name_cor: str, optional
            Name of the plot for the numerical features. The default is corheatmap.

        Returns
        -------
        list : plt.figure, axes.Axes, p <Object containing both figure and axes>
        A list containing the figure and axes of each drawn plot.

        Example
        --------
        > relation(df = health_data, gtype = 2, path = "/Users/Person/Documents",
        name_cor = "numerical_heatmap")
    """
    to_return = []
    if gtype != 2:
        chi = []
        cols = df.columns
        num_cols = df._get_numeric_data().columns
        cat_cols = list(set(cols) - set(num_cols))
        for i in cat_cols:
            for j in cat_cols:
                con = pd.crosstab(df[i], df[j])
                c, p, dof, expected = stats.chi2_contingency(con)
                chi.append(round(p, 3))
        data = np.array(chi)
        n = int(np.sqrt(len(data)))
        data = data.reshape(n, n)

        fig, ax = plt.subplots(figsize=(14, 14))
        p = sns.heatmap(data=data, annot=True, fmt='2g', ax=ax,
                        cmap=cm.YlOrBr, xticklabels=cat_cols, yticklabels=cat_cols)

        if path is not None:
            fig.savefig(f'{path}/{name_chi}.png', format='png', bbox_inches='tight')
        plt.show()
        # pandas.DataFrame(chi, chi_cols, chi_cols)
        to_return.append([fig, ax])
    if gtype != 1:
        plt.figure(figsize=(14, 14))
        p = sns.heatmap(df.corr(), annot=True)
        fig = p.get_figure()
        if path is not None:
            fig.savefig(f'{path}/{name_cor}.png', format='png', bbox_inches='tight')
        plt.show()
        to_return.append(p)
    return to_return


def survival_analysis(time, censor_status, group, input_data: pd.DataFrame):
    """
    Show the kaplan-meier curve and combine with a median survival time summary.
    Function for survival data analysis.

        Parameters
        ----------
        time : names of time variables in input_data, mandatory
            Time to event of interest.
        censor_status : names of variables in input_data, mandaory
            True(1) if the event of interest was observed, False(0) if the event was
            lost (right-censored).
        group : names of time variables in input_data, mandatory
            Grouping variables that will produce plottings and summary tables with
            different colors (e.g. treatment group).
        input_data : pd.DataFrame, mandatory
            Input dataset name.

        Returns
        -------
        fig, ax :  Figure, axes.Axes
        The matplotlib figure and ax containing the plot and summary table.


        Examples
        --------
        > survival_analysis(time="time_to_event", censor_status="censor",
        group="treatment", input_data=data)

    """
    # remove records with missing time-to-event value
    ana_data = input_data[input_data[time].notnull()]
    group_list = ana_data.sort_values(by=[group])[group].unique()
    # set up figure, ax
    fig, ax = plt.subplots(figsize=(8, 6))
    temp = pd.DataFrame()
    # iterate through group
    for i in group_list:
        # data filter
        mask = ana_data[group] == i
        # draw KM plot
        kmf = KaplanMeierFitter()
        kmf.fit(ana_data[time][mask], ana_data[censor_status][mask], label=i)
        kmf.plot_survival_function(ax=ax)
        # get median survival time
        row = pd.DataFrame([[i, kmf.median_survival_time_]],
                           columns=[group, "Median Survival Time"])
        temp = pd.concat([temp, row])
    # combine median survival table with plot
    plt.table(cellText=temp.values, colLabels=(group, "Median survival time"),
              loc='bottom', bbox=[0, -0.6, 1, 0.4], cellLoc="center")
    # plot format adjust
    plt.title(f"Survival of different {group}")
    plt.subplots_adjust(left=0.2, bottom=0.35)

    return fig, ax


def boxplot_grid(df, col1=None, col2=None, col3=None):
    """
    A function for creating a grid of box plots with two options. One being that
    no column was specified, in this case the grid will be box plots of all numeric
    features in the dataset. The other being that three columns were specified, with
    one column being numeric and the others being categorical. In this case the grid
    will be of the numeric value on the basis of the two categorical values. If all
    three columns are specified, then the first case will be preformed.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset holding the data that will be plotted.
        col1 : str, optional
            The categorical column that the grid will be split based on.
        col2 : str, optional
            The categorical column on the x-axis of each plot.
        col3 : str, optional
            The numerical column on the y-axis of each plot.

        Returns
        -------
        fig, ax :  Figure, array of axes.Axes
        The matplotlib figure and axes containing the plots.


        Examples
        --------
        > boxplot_grid(df=health_data, col1="months", col2="sex", col3="BMI")

    """
    if col1 is None or col2 is None or col3 is None:
        num_cols = df._get_numeric_data().columns
        sizex = int(math.sqrt(len(num_cols)))
        marg = (len(num_cols) - (sizex * sizex)) / sizex
        if marg.is_integer():
            sizey = sizex + int(marg)
        else:
            sizey = sizex + int(marg) + 1
        plt.style.use('ggplot')
        fig, axes = plt.subplots(sizey, sizex, figsize=(20, 20))
        for i in range(len(num_cols)):
            sns.boxplot(df[num_cols[i]], ax=axes.flat[i])
            axes.flat[i].title.set_text(num_cols[i])
        fig.tight_layout()
        return fig, axes
    elif col1 is not None and col2 is not None and col3 is not None:
        ordered = sorted(df[col1].unique())
        wrap = int(math.sqrt(len(ordered)))
        g = sns.FacetGrid(df, col=col1, col_order=ordered, col_wrap=wrap)
        g.map(sns.boxplot, col2, col3, palette='muted')
        for ax in g.axes.flatten():
            ax.tick_params(labelbottom=True)
        plt.tight_layout()
        plt.show()
        return g


def pie(df, col, path=None, name='pie_chart'):
    """
    Draws a pie chart of the specified column. If the path is given the png file of
    the chart will be saved under the name of pie_chart.png at the specified path.
    This chart should be used for columns with discrete values.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset that contains the feature that will be plotted.
        col : str, mandatory
            The name of the column containing the feature to be plotted.
        path : str, optional
            Path to the directory that the png file of the chart will be
            saved in. If left empty, the file will not be saved.
        name : str, optional
            Name of the png image of the chart. The default is pie_chart.

        Returns
        -------
        ax : axes.Axes
        The axes of the plot.

        Example
        --------
        > pie(df = demographic_data, col = "sex",
        path = "/Users/Person/Documents", name = "demo_pie")
    """
    total = df[col].value_counts().values.sum()

    def fmt(x):
        return '{:.1f}%\n{:.0f}'.format(x, total * x / 100)

    colors = sns.color_palette("Spectral")
    plt.figure(figsize=(20, 20))
    ax = plt.pie(df[col].value_counts().values, colors=colors, labels=df[col].value_counts().index, autopct=fmt)
    if path is not None:
        plt.savefig(f'{path}/{name}.png', format='png', bbox_inches='tight')
    return ax
