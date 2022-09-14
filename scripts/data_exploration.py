import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class dataExplorer:

    ###VISUALIZATION###

    def plot_heatmap(df: pd.DataFrame, title: str, cbar=False) -> None:
        
        '''
        Plots rectangular matrix as a color encoded matrix 
        heatmap of the dataframe(df)
        [cbar=False]=>dont draw colorbar
        [title]=>pass title of the plot here
        '''
        plt.figure(figsize=(13, 8))
        sns.heatmap(df, annot=True, cmap='viridis', vmin=0,
                    vmax=1, fmt='.2f', linewidths=.7, cbar=cbar)
        plt.title(title, size=20, fontweight='bold')
        plt.show()
        
    
    def plot_heatmap_from_correlation(correlation, title:str):
        
        '''Plots rectangular matrix as a color encoded matrix 
        and correlation matrix passed to the correlation argument.
        
        '''
        
        plt.figure(figsize=(14,9))
        sns.heatmap(correlation)
        plt.title(title, size=18, fontweight='bold')
        plt.show()
        
        
    def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str, hue: str, style: str) -> None:
        
        '''
        Plots data as a scatter plot of df 
        as [x_col] x-axis column and [y_col] y-axis column
        [hue]: hue column
        '''
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue, style=style)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
        
        
    def simple_plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> None:
        
        '''
        same as plot_scatter. Just no hue column
        '''
        plt.figure(figsize=(12, 7))
        sns.scatterplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
        
    def plot_hist(df: pd.DataFrame, column: str, color: str) -> None:
        
        '''
        Plots a histogram of df with [column] parameter(the column to be plotted)
        [color]: color of the histogram
        '''
        sns.displot(data=df, x=column, color=color, kde=True, height=7, aspect=2)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()
        
    def plot_bar(df: pd.DataFrame, x_col: str, y_col: str, title: str, xlabel: str, ylabel: str) -> None:
        
        '''
        Plots a bar chart of df as 
        [x_col] x-axis column and [y_col] y-axis column
        
        [xlabel]: x-axis label
        [ylabel]: y-axis label
        '''
        plt.figure(figsize=(12, 7))
        sns.barplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.xlabel(xlabel, fontsize=16)
        plt.ylabel(ylabel, fontsize=16)
        plt.show()
        
        
    def plot_box(df: pd.DataFrame, x_col: str, title: str) -> None:
        
        '''
        Plots a box plot of df as [x_col] x-axis column
        
        '''
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.show()
        
        
    def plot_box_multi(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> None:
        
        '''
        same as plot_box but adds [y_col] y-axis column
        '''
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=df, x=x_col, y=y_col)
        plt.title(title, size=20)
        plt.xticks(rotation=75, fontsize=14)
        plt.yticks(fontsize=14)
        plt.show()
        
    
    def plot_count(df: pd.DataFrame, column: str) -> None:
        
        '''
        Plots a count plot of df
        
        column: column to be plotted
        '''
        plt.figure(figsize=(12, 7))
        sns.countplot(data=df, x=column)
        plt.title(f'Distribution of {column}', size=20, fontweight='bold')
        plt.show()



    
        