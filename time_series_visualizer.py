import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
import matplotlib.dates as mdates

register_matplotlib_converters()

# Import data 
df = pd.read_csv('fcc-forum-pageviews.csv')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(20, 6))
    
    # Convert the date column to datetime format (if it's not already)
    df["date"] = pd.to_datetime(df["date"])
    
    # Plot the data
    ax.plot(df["date"], df["value"], color='r', linewidth=2)
    
    # Set the title and axis labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Use MonthLocator to label every month and YearLocator to label every year
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    
    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    # Save image and return fig 
    fig.savefig('line_plot.png')
    return fig
 

def draw_bar_plot(): 
   
    # Prepare data for box plots 
    df_bar = df.copy()
    df_bar['year'] = pd.DatetimeIndex(df_bar['date']).year
    df_bar['month'] = pd.DatetimeIndex(df_bar['date']).month
    df_bar['month'] = df_bar['month'].apply(lambda x: calendar.month_name[x])

  
    # Copy and modify data for monthly bar plot
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index(name='avg_views')

    # Pivot the data to create a grouped bar plot
    df_pivot = df_bar.pivot(index='year', columns='month', values='avg_views')

    df_pivot = df_pivot[['January', 'February', 'March', 'April', 'May', 'June', 
    'July', 'August', 'September', 'October', 'November', 'December']]
    # Create an unstacked bar plot for each year
    ax = df_pivot.plot(kind='bar', figsize=(12, 12), width=0.8)

    # Add some text for labels and title
    ax.set_ylabel("Average Page Views")
    ax.set_xlabel("Years")
    ax.set_title("Average Page Views by Month and Year")

    # Customize the legend
    ax.legend(title='Months', loc='upper left', bbox_to_anchor=(1, 1))

    plt.tight_layout()

    # Save image and return fig
    fig = plt.gcf()
    fig.savefig('bar_plot.png')

    return fig
  
def draw_box_plot(): 

    # Prepare data for box plots 
    df_box = df.copy()

    # Add the month and year coloumns 
    df_box['year'] = pd.DatetimeIndex(df_box['date']).year
    df_box['month'] = pd.DatetimeIndex(df_box['date']).month
    df_box['month'] = df_box['month'].apply(lambda x: calendar.month_abbr[x])
  

    df_box = df_box.groupby(['year','month'])['value'].mean().reset_index(name='views')

    # Draw box plots (using Seaborn)
    fig, axs = plt.subplots( 1, 2, figsize = ( 21,  7))
    sns.boxplot(data=df_box, x="year", y="views", ax=axs[0])
    custom_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    sns.boxplot(data=df_box, x="month", y="views", ax=axs[1], order=custom_order)
    axs[0].set_title("Year-wise Box Plot (Trend)")
    axs[0].set_xlabel("Year")
    axs[0].set_ylabel("Page Views")
    axs[1].set_title("Month-wise Box Plot (Seasonality)")
    axs[1].set_xlabel("Month")
    axs[1].set_ylabel("Page Views")
    custom_y_ticks = [0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000, 200000]
    axs[0].set_yticks(custom_y_ticks)
    axs[0].set_yticklabels(custom_y_ticks)
    axs[1].set_yticks(custom_y_ticks)
    axs[1].set_yticklabels(custom_y_ticks)
    
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
