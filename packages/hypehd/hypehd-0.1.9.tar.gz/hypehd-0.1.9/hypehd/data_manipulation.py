import pandas as pd
import numpy as np
from operator import itemgetter
import datetime as dt


def handle_null(input_data, col, impute_type, by_vars=None):
    """
         Replace missing values with a descriptive statistic.

                Parameters
                ----------
                input_data : pd.DataFrame
                    Input dataset name.
                col : str
                    Variable name need to be imputed.
                by_vars : str or list
                    Grouping variables uniquely identifying a set of records for computing descriptive statistic .
                impute_type : str, select from (mean, max, min, median, remove-remove rows with null)
                    The imputation method.

                Returns
                -------
                input_data : pd.DataFrame
                Same dataset after imputation.

                Examples
                --------
                > df = pd.DataFrame()
                > df['C0'] = [0.2601,0.2358,0.1429,0.1259,0.7526,0.7341,0.4546,0.1426,0.1490,0.2500]
                > df['C1'] = [0.7154,np.nan,0.2615,0.5846,np.nan,0.8308,0.4962,np.nan,0.5340,0.6731]
                > handle_null(input_data=df, col="C1", impute_type="median")

    """
    output_data = input_data.copy()
    # when there is by variables
    if by_vars is not None:
        if impute_type.lower() == 'mean':
            output_data[col].fillna(output_data.groupby(by_vars)[col].transform('mean'), inplace=True)
        elif impute_type.lower() == 'median':
            output_data[col].fillna(output_data.groupby(by_vars)[col].transform('median'), inplace=True)
        elif impute_type.lower() == 'min':
            output_data[col].fillna(output_data.groupby(by_vars)[col].transform('min'), inplace=True)
        elif impute_type.lower() == 'max':
            output_data[col].fillna(output_data.groupby(by_vars)[col].transform('max'), inplace=True)
    # when there is no by variables
    else:
        if impute_type.lower() == 'mean':
            output_data[col].fillna(output_data[col].mean(), inplace=True)
        elif impute_type.lower() == 'median':
            output_data[col].fillna(output_data[col].median(), inplace=True)
        elif impute_type.lower() == 'min':
            output_data[col].fillna(output_data[col].min(), inplace=True)
        elif impute_type.lower() == 'max':
            output_data[col].fillna(output_data[col].max(), inplace=True)
        elif impute_type.lower() == "remove":
            output_data.dropna(axis=0, subset=[col], inplace=True)

    return output_data


def change_type(df, col, col_type):
    """
    Changes the data type of the specified column of a data frame.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset that will be changed.
        col : str, mandatory
            Name of the chosen column.
        col_type : data type, mandatory
            Type to change to. The available options are int, float and str.

        Returns
        -------
        df : pd.DataFrame
            The dataset with changed column type.

        Examples
        --------
        > data = change_type(data, 'sbp', int)
    """
    if col_type == str:
        df[col] = df[col].apply(lambda x: str(x))
    elif col_type == int:
        if type(df[col][0]) == str:
            df[col] = df[col].apply(lambda x: int(x.replace(',', '')
                                                  .replace(' ', '')))
        else:
            df[col] = df[col].apply(lambda x: int(x))
    elif col_type == float:
        if type(df[col][0]) == str:
            df[col] = df[col].apply(lambda x: float(x.replace(',', '')
                                                    .replace(' ', '')))
        else:
            df[col] = df[col].apply(lambda x: float(x))
    else:
        print('Type unsupported')
    return df


def data_selection(input_data: pd.DataFrame, cond=None, keep_col=None, drop_col=None, sort_by=None, merge_data=None,
                   merge_by=None, merge_keep_col=None, sort_asc=True, rename=None):
    """
    Return a new data frame of given selection crateria.

            Parameters
            ----------
            input_data : pd.DataFrame
                Input dataset name.
            cond : str, optional
                The query string to filter input_data.
            keep_col : list or str, optional
                The variable names in input_data which user want to keep.
            drop_col : list or str, optional
                The variable names in input_data which user want to drop.
            sort_by : list or str, optional
                The variable names in input_data or merge_data after keeping and dropping which user want to sort the
                data frame.
            merge_data : pd.DataFrame or Series, optional
                Merge DataFrame or named Series objects with a database-style join. Default type of merge is left.
            merge_by : list or str, optional
                Column names to join on.
            merge_keep_col : list or str, optional
                The variable names in merge_data which user want to keep.
            sort_asc : bool or list of bool, default True, optional
                Sort ascending vs. descending. Specify list for multiple sort orders.
            rename : dict
                Change columns labels. Specify the original column names and alter names in the dict object.

            Returns
            -------
            output_data : pd.DataFrame
            Dataset with the selection creteria applied.

    """
    # filter the data
    if cond is not None:
        output_data = input_data.query(cond)
    else:
        output_data = input_data
    # keep variables
    if keep_col is not None:
        output_data = output_data.loc[:, keep_col]
    # drop variables
    if drop_col is not None:
        output_data = output_data.drop(drop_col, axis=1)
    # keep variables in merge dataset
    if merge_keep_col is not None:
        merge_data = merge_data.loc[:, merge_keep_col]
    # merge dataset with input dataset
    if merge_data is not None:
        output_data = output_data.merge(merge_data, on=merge_by, how="left")
    # sort dataset
    if (sort_by is not None) & isinstance(output_data, pd.DataFrame):
        output_data.sort_values(sort_by, ascending=sort_asc, inplace=True)
    elif sort_by is not None:
        output_data = output_data.sort_values(ascending=sort_asc).copy()
    # rename columns in dataset
    if rename is not None:
        output_data.rename(columns=rename, inplace=True)

    return output_data


def derive_baseline(input_data, base_visit, by_vars: list, value, chg=True, pchg=True):
    """
        Return a new data frame of derived baseline and related variables. Function for longitudinal
        data analysis.

                Parameters
                ----------
                input_data : pd.DataFrame
                    Input dataset name.
                base_visit : str
                    The query string to specify the baseline visit. (e.g. 'visit==0').
                by_vars : list
                    Grouping variables uniquely identifying a set of records for baseline and related variables.
                value : str
                    The variable names from which to extract the baseline value.
                chg : bool, default to True
                    If True, return change from baseline (chg) variable as value - base.
                pchg : bool, default to True
                    If True, return percent change from baseline (chg) variable as (value - base)/base.

                Returns
                -------
                output_data : pd.DataFrame
                Dataset with derived baseline and related variables.

                See also
                -------
                derive_extreme_flag

                Examples
                --------
                > derive_baseline(input_data=data, base_visit='visit==0', by_vars=["patient","lab test"], value=value,
                > chg=True, pchg=True)

    """
    combine_col = by_vars + [value]
    # get baseline records
    baseline = data_selection(keep_col=combine_col, input_data=input_data,
                              cond=base_visit, rename={value: "base"})
    # merge baseline records with input dataset
    output_data = data_selection(input_data=input_data, merge_data=baseline, merge_by=by_vars)
    # derive chg/pchg variables
    if chg:
        output_data["chg"] = output_data[value] - output_data["base"]
    if pchg:
        output_data["pchg"] = (output_data[value] - output_data["base"]) / output_data["base"]

    return output_data


def derive_extreme_flag(input_data, by_vars: list, sort_var: list, new_var, mode, value_var=None):
    """
        Add a variable flagging the specified observation within each by_vars group. Function for longitudinal
        data analysis.

                Parameters
                ----------
                input_data : pd.DataFrame
                    Input dataset name.
                by_vars : list
                    Grouping variables uniquely identifying a set of records for flags.
                sort_var : list
                    Sort variables used to sort the dataset which help find the first/last.
                new_var : str
                    The name of variable to add. It is set to "Y" for the observation (depending on the mode)
                    of each by group.
                mode : str, select from (last, first, max, min)
                    Determines of the first/last/max/min observation is flagged.
                value_var : str
                    The variable names from which to extract the specified value.

                Returns
                -------
                output_data : pd.DataFrame
                Dataset with derived extreme variables.

                Examples
                --------
                > derive_extreme_flag(input_data=data, by_vars=["patient","lab_test"],
                > sort_var=["patient","lab test", "test_value"], new_var="first_flag",
                > mode="first", value_var="test_value")

    """
    if mode.lower() == "last":
        temp = input_data.sort_values(sort_var).groupby(by_vars).last()
    elif mode.lower() == "first":
        temp = input_data.sort_values(sort_var).groupby(by_vars).first()
    elif mode.lower() == "max":
        temp = input_data.loc[input_data.sort_values(sort_var).groupby(by_vars)[value_var].idxmax(), :]
    elif mode.lower() == "min":
        temp = input_data.loc[input_data.sort_values(sort_var).groupby(by_vars)[value_var].idxmin(), :]
    temp[new_var] = "Y"
    output_data = data_selection(input_data, merge_data=temp.reset_index(), merge_by=by_vars + sort_var,
                                 merge_keep_col=by_vars + sort_var + new_var.split())

    return output_data


def time_to_event(input_data, start_date, end_date, censor_date, new_var, unit):
    """
        Add a variable flagging the specified observation within each by_vars group. Function for survival
        data analysis.

                Parameters
                ----------
                input_data : pd.DataFrame
                    Input dataset name.
                start_date : str
                    Variable name of time to event origin date.
                end_date : str
                    Variable name of time to event happened date.
                censor_date : str
                    Variable name of time to event censoring date.
                new_var : str
                    The name of variable to add.
                unit : str, select from (day, week, month, year)
                    The unit of time to event duration.

                Returns
                -------
                output_data : pd.DataFrame
                Dataset with derived extreme variables.

                Examples
                --------
                > derive_extreme_flag(input_data=data, by_vars=["patient","lab_test"],
                > sort_var=["patient","lab test", "test_value"], new_var="first_flag",
                > mode="first", value_var="test_value")

    """
    # change variables type into datetime
    output_data = input_data.copy()
    if not isinstance(start_date, dt.datetime):
        output_data[start_date] = pd.to_datetime(output_data[start_date], infer_datetime_format=True)
        output_data[end_date] = pd.to_datetime(output_data[end_date], infer_datetime_format=True)
        output_data[censor_date] = pd.to_datetime(output_data[censor_date], infer_datetime_format=True)

    # derive time_to_event variable
    output_data[new_var] = np.where((output_data[start_date].notnull()) & (output_data[end_date].notnull()),
                                    output_data[end_date] - output_data[start_date],
                                    output_data[censor_date] - output_data[start_date])
    # derive censor variable
    output_data['censor_status'] = np.where((output_data[start_date].notnull()) & (output_data[end_date].notnull()), 1,
                                            0)

    # format value based on unit
    if unit.lower() == 'day':
        output_data[new_var] = output_data[new_var].dt.days
    elif unit.lower() == 'week':
        output_data[new_var] = round(output_data[new_var].dt.days / 7, 2)
    elif unit.lower() == 'month':
        output_data[new_var] = round(output_data[new_var].dt.days / 30, 2)
    elif unit.lower() == 'year':
        output_data[new_var] = round(output_data[new_var].dt.days / 365.25, 2)
    output_data['unit'] = unit

    return output_data


def read(source, path=None, sheet_name=None, sql=None, con=None):
    """
    Reads data from specified path into a pandas dataframe.

        Parameters
        ----------
        source : str, mandatory
            The type of the data source. Available options are csv, tsv, excel, sql,
            json, html and xml.
        path : str, optional
            The path to the data.
        sheet_name : str, optional
            Name of the excel sheet. The path to the excel file need to be specified
            for this option.
        sql : str/SQLAlchemy Selectable, optional
            The sql command for getting the data.
        con: SQLAlchemy connectable/str/sqlite3 connection, optional
            Connection to database.

        Returns
        -------
        df : pd.DataFrame
            The dataset.

        Examples
        --------
        > from sqlite3 import connect
        > conn = connect(':memory:')
        > data = read(source='sql', sql='SELECT int_column, date_column FROM test_data',
        con=conn)
    """
    df = pd.DataFrame()
    source = source.lower()
    if source == 'csv':
        df = pd.read_csv(path)
    elif source == 'tsv':
        df = pd.read_csv(path, sep='\t')
    elif source == 'excel':
        if sheet_name is None:
            df = pd.read_excel(path)
        else:
            df = pd.read_excel(io=path, sheet_name=sheet_name)
    elif source == 'json':
        df = pd.read_json(path)
    elif source == 'html':
        df = pd.read_html(path)
    elif source == 'xml':
        df = pd.read_spss(path)
    elif source == 'sql' and sql is not None and con is not None:
        pd.read_sql(sql, con)
    else:
        print("Source type not supported")
    return df


def check_bias(df, col=None, real_dist=None, n_marg=10, marg=5):
    """
    Checks data for two types of bias. Too many null values and improper distribution.
    If no column is specified, only the amount of null values will be checked.
    The function prints the column names with too many null values along with the number
    of null values and The names of columns with skewed distribution along with their 
    distribution.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The dataset containing the column of interest.
        col : str, optional
            The name of the column to check.
        real_dist : list of lists, mandatory
            A list containing two item lists of the values and their proper distribution.
        n_marg : int, optional
            The percentage of null values that is allowed. The default is 10.
        marg : int, optional
            The amount of deviance allowed from the proper distribution.

        Returns
        -------
        too_nul : list of columns that have too many null values
        skew : list of columns with skewed distribution

        Examples
        --------
        > check_bias(df=data, col='Blood_cell_type', real_dist=[['Red', 37],['White', 53]],
         n_marg=50)
    """
    nul = df.isna().sum()
    too_nul = []
    n_marg = n_marg/100
    leng = df.shape[0]
    i = 0
    skew = []
    skewed = []
    for n in nul:
        if n >= n_marg * leng:
            too_nul.append([df.columns[i], n])
        i += 1
    print('Columns with too many null values: \n', too_nul)
    if real_dist is not None and col is not None:
        count = df[col].value_counts(ascending=False).rename_axis(
            'vals').reset_index(name='dist')
        count.index.name = 'Index'
        count['dist'] = count['dist'] * 100 / len(df)
        for i in range(0, len(real_dist)):
            dist = count.loc[count['vals'] == real_dist[i][0]]
            real = real_dist[i][1]
            ours = dist['dist'].values[0]
            if ours > (real + marg) or ours < (real - marg):
                skew.append(dist)
        print("\nColumns with skewed distribution:")
        for i in skew:
            print(str(i['vals'].values[0]) + " : " + str(i['dist'].values[0]))
            skewed.append(str(i['vals'].values[0]))
            skewed.append(i['dist'].values[0])
    return too_nul, skewed


def numeric_to_categorical(df, col: str, bounds, add=False):
    """
    Changes numeric data to categories. If add option if True the data will be added
    into a separate column and if it is False the categorical values will replace the
    numerical values of the column.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The data source.
        col : str, mandatory
            The name of the column to change.
        bounds : list of lists, mandatory
            A list containing two item lists of the upper bound of each category (int)
            and the category name (str).
        add : str, optional
            Choice of adding results as an additional column or replacing the current
            column. The default is False (replacement).

        Returns
        -------
        df : pd.DataFrame
            The changed dataset.

        Examples
        --------
        > data = numeric_to_categorical(data, 'sbp', [[9,'low'],[1000000,'high']],True)
    """
    def group(row, bound, column):
        bound = sorted(bound, key=itemgetter(0))
        for i in bound:
            if float(row[column]) <= i[0]:
                return i[1]

    if add:
        name = col + '_group'
        df[name] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df
    else:
        df[col] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df


def categorical_to_numeric(df, col: str, bounds, add=False):
    """
    Changes categories to numbers. If add option if True the data will be added
    into a separate column and if it is False the categorical values will replace the
    categorical values of the column.

        Parameters
        ----------
        df : pd.DataFrame, mandatory
            The data source. 
        col : str, mandatory
            The name of the column to change.
        bounds : list of lists, mandatory
            A list containing two item lists of the name of the categorical column
            and the number to replace it with.
        add : str, optional
            Choice of adding results as an additional column or replacing the current
            column. The default is False (replacement).

        Returns
        -------
        df : pd.DataFrame
            The changed dataset.

        Examples
        --------
        > data = categorical_to_numeric(data, 'sex', [['Female', 0],['Male', 1]],True)
    """
    def group(row, bound, column):
        bound = sorted(bound, key=itemgetter(0))
        for i in bound:
            if row[column] == i[0]:
                return i[1]

    if add:
        name = col + '_num'
        df[name] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df
    else:
        df[col] = df.apply(lambda row: group(row, bounds, col), axis=1)
        return df
