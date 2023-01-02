from sklearn.decomposition import PCA
import pandas as pd
import seaborn as sns
import plotly.express as px
from sklearn.manifold import TSNE
from matplotlib import animation
import matplotlib.pyplot as plt
from radar import *
from sklearn.preprocessing import StandardScaler, MinMaxScaler


cluster_colors = ['#b4d2b1', '#568f8b', '#1d4a60', '#cd7e59', '#ddb247', '#d15252', '#b4d200','#6f8f8b','#cd7e00','#dd525f']



def prepare_pca(n_components, data, cluster_labels):
    names = ['x', 'y', 'z']
    matrix = PCA(n_components=n_components).fit_transform(data)
    df_matrix = pd.DataFrame(matrix)
    df_matrix.rename({i:names[i] for i in range(n_components)}, axis=1, inplace=True)
    df_matrix['labels'] = cluster_labels
    return df_matrix
    
def prepare_tsne(n_components, data, cluster_labels):
    names = ['x', 'y', 'z']
    matrix = TSNE(n_components=n_components).fit_transform(data)
    df_matrix = pd.DataFrame(matrix)
    df_matrix.rename({i:names[i] for i in range(n_components)}, axis=1, inplace=True)
    df_matrix['labels'] = cluster_labels

    return df_matrix

def plot_tsne(tsne_data, cluster_labels):
    df_tsne = pd.DataFrame(tsne_data).rename({0: 'x', 1: 'y'}, axis=1)
    df_tsne['z'] = cluster_labels
    sns.scatterplot(x=df_tsne.x, y=df_tsne.y, hue=df_tsne.z, palette="Set2")
    plt.show()

def plot_3d(df, name ='Cluster'):
    fig = px.scatter_3d(df, x='x', y='y', z='z', color=name, opacity=0.5)
    fig.update_traces(marker=dict(size=3))
    fig.show()

def plot_animation(df, label_column, name):
    def update(num):
        ax.view_init(200, num)

    N=360
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['x'], df['y'], df['z'], c=df[label_column],
               s=6, depthshade=True, cmap='Paired')
    ax.set_zlim(-25, 35)
    ax.set_xlim(-40, 40)
    plt.tight_layout()
    ani = animation.FuncAnimation(fig, update, N, blit=False, interval=50)
    ani.save('{}.gif'.format(name), writer='imagemagick')
    plt.show()


def pca_scatterplot(data, new_data,cluster_type):
    plt.figure()
    pca_df = prepare_pca(3, data, new_data[cluster_type])
    sns.scatterplot(x=pca_df.x, y=pca_df.y, hue=pca_df.labels, size =pca_df.labels, sizes = (40,400),palette="Set3", legend = 'full', alpha = .5)
    plt.gcf().canvas.set_window_title('2D Scatter Plot with PCA')
    plt.show()

def radar_plot(data, new_data, cluster_type):
    scaler = StandardScaler()
    X_std = scaler.fit_transform(new_data)
    X_std = pd.DataFrame(X_std, columns=new_data.columns)
    fig = plt.figure(figsize=(8, 8))
    no_features = len(data.columns)
    radar = Radar(fig, data.columns, np.unique(new_data[cluster_type]))

    for k in range(len(np.unique(new_data[cluster_type]))):
        cluster_data = X_std.iloc[k].values.tolist()
        radar.plot(cluster_data,  '-', lw=2, color=cluster_colors[k], alpha=0.2, label='cluster {}'.format(k))

    radar.ax.legend()
    radar.ax.set_title("Cluster characteristics: Feature means per cluster", size=22, pad=60)
    plt.gcf().canvas.set_window_title('Radar Plot for our Clusters')
    plt.show()

def box_plots(data, new_data, cluster_type):
    features = data.columns
    ncols = 4
    nrows = len(features) // ncols + (len(features) % ncols > 0)
    fig = plt.figure(figsize=(15,15))

    for n, feature in enumerate(features):
        ax = plt.subplot(nrows, ncols, n + 1)
        box = new_data[[feature, cluster_type]].boxplot(by=cluster_type,ax=ax,return_type='both',patch_artist = True)

        for row_key, (ax,row) in box.iteritems():
            ax.set_xlabel('Cluster')
            ax.set_title(feature,fontweight="bold")
            for i,box in enumerate(row['boxes']):
                box.set_facecolor(cluster_colors[i])

    fig.suptitle('Feature distributions per cluster', fontsize=18, y=1)   
    plt.tight_layout()
    plt.gcf().canvas.set_window_title('Box Plot for our Clusters')
    plt.show()

def bar_plot(data, new_data, cluster_type):
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(data))
    df_scaled.columns = data.columns
    df_scaled[cluster_type] = new_data[cluster_type]
    results = pd.DataFrame(columns=['Variable', 'Std'])
    df_mean = df_scaled.loc[df_scaled[cluster_type]!=-1, :].groupby(cluster_type).mean().reset_index()

    for column in df_mean.columns[1:]: #on ne prend pas la colonne dbscan
        results.loc[len(results), :] = [column, np.std(df_mean[column])]
    selected_columns = list(results.sort_values('Std', ascending=False).head(5).Variable.values) + [cluster_type]
    # Plot data
    tidy = df_scaled[selected_columns].melt(id_vars=cluster_type)
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x=cluster_type, y='value', hue='variable', data=tidy, palette='Set3')
    plt.legend(loc='upper right')
    plt.savefig("agnes_results.jpg", dpi=300)
    plt.gcf().canvas.set_window_title('Bar Plot for our Clusters')
    plt.show()


def plot_3dd(data, new_data, cluster_type):
    tsne_3d_df = prepare_tsne(3, data, new_data[cluster_type])
    tsne_3d_df[cluster_type] = [str(label) for label in new_data[cluster_type]]
    plot_3d(tsne_3d_df, name=cluster_type)
    if cluster_type =='Cluster_dbscan':
        tsne_3d_df.agnes = tsne_3d_df.agnes.astype(int)
        plot_animation(tsne_3d_df, cluster_type, 'dbscan_new')
    else:
        tsne_3d_df.agnes = tsne_3d_df.agnes.astype(float)
        tsne_3d_df.agnes = tsne_3d_df.agnes.astype(int)
        plot_animation(tsne_3d_df, cluster_type, 'agnes_new')
