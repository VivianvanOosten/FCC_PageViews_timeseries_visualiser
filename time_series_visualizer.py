import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.index = df['date']
df = df[['value']]

# Clean data
df_clean = df[df['value'] <= df['value'].quantile(0.975)]
df = df_clean[df_clean['value'] >= df_clean['value'].quantile(0.025)]
df.sort_values(by=['date'],inplace=True)


def draw_line_plot():
    # Draw line plot
  df_line = df.reset_index()
  fig = plt.figure(figsize=(20,5))
  plt.plot(df_line['date'],df_line['value'], c='r')
  plt.ylabel('Page Views')
  plt.xlabel('Date')
  plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig



def draw_bar_plot():
    # Copy and modify data for monthly bar plot
  df_bar = df
  df_bar = df_bar.reset_index()
  df_bar['year'] = [d.year for d in df_bar.date]
  df_bar['month'] = [d.strftime('%B') for d in df_bar.date]
  months = ['January','February','March','April','May','June','July','August','September','October','November','December']
  df_pivoted = df_bar.groupby(['month','year']).mean().reset_index()
  df_pivoted = pd.pivot(df_pivoted, index='year',columns='month',values='value').reset_index()

  fig = df_pivoted.plot(x='year', kind='bar', stacked=False,xlabel='Years', ylabel='Average Page Views').get_figure()
  plt.legend(labels = months)

  # plt.bar(df_bar, IT, color ='r', width = barWidth,
  #       edgecolor ='grey', label ='IT')
  # plt.bar(br2, ECE, color ='g', width = barWidth,
  #         edgecolor ='grey', label ='ECE')
  # plt.bar(br3, CSE, color ='b', width = barWidth,
  #         edgecolor ='grey', label ='CSE')

    # Draw bar plot

    # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.reset_index()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box.sort_values(by='date',inplace=True,ascending=True)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    print(df_box.head())

    months2 = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(10,5))

    sns.boxplot(x = df_box['year'], y = df_box['value'], ax = ax1)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')
    ax1.set_title('Year-wise Box Plot (Trend)')


    sns.boxplot(x = df_box['month'], y = df_box['value'], ax = ax2, order = months2)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    fig.savefig('box_plot.png')
    return fig
