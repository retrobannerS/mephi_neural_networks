import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == '__main__':
    data = pd.concat([pd.read_csv('data/segmentation.test'), pd.read_csv('data/segmentation.data')])
    data.rename(columns=lambda x: x.lower(), inplace=True)
    nominal_features = ['short-line-density-5', 'short-line-density-2']


    print(len(data))

    for column in data.columns[0:]:
        dc = data[column]
        values = dc.values
        plt.suptitle(column)
        plt.subplot(1, 2, 1)
        plt.boxplot(values)
        plt.subplot(1, 2, 2)
        plt.hist(values, 30)
        # plt.savefig(f'images/{column}.png')
        plt.clf()

        if column not in nominal_features:
            mean = dc.mean()
            std = dc.std()
            u = mean + 5*std
            l = mean - 5*std
            outliers_count = (dc < l).sum() + (dc > u).sum()
            print(f'{column} outliers count: ', outliers_count)

            if outliers_count > 0:
                data = data[dc >= l]
                data = data[dc <= u]

    print(len(data))

    corr = data.corr()
    sns.heatmap(corr, linewidth=0.5, annot=True)
    plt.tight_layout()
    plt.show()
    plt.clf()

    corr_pairs = [
        ('intensity-mean', 'rawred-mean'),
        ('intensity-mean', 'rawblue-mean'),
        ('intensity-mean', 'rawgreen-mean'),
        ('intensity-mean', 'rawred-mean'),
        ('hue-mean', 'region-centroid-row'),
        ('short-line-density-2', 'vedge-mean'),
        ('vedge-mean', 'hedge-mean')
    ]

    for c1, c2 in corr_pairs:
        v1 = data[c1].values
        v2 = data[c2].values

        plt.scatter(v1, v2)
        plt.suptitle(f'{c1} to {c2}')
        plt.tight_layout()
#        plt.savefig(f'images/{c1} to {c2}.png')
        plt.clf()

