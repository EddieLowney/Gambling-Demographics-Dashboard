import gambling_stats
import seaborn as sns
import matplotlib.pyplot as plt
def create_violin(df, category, data):
    fig, ax = plt.subplots()
    sns.violinplot(data=df, x=category, y=data, ax=ax, log_scale=True)
    plt.show()  # Display the plot
    return fig


fig1 = create_violin(gambling_stats.merged_df, 'Gender', 'loss')


