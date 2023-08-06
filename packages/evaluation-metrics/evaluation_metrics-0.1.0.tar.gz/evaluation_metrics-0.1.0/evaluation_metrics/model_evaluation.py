import pandas as pd


class ModelEvaluation:

    """
    A class to compute the ks, auc score & gini of the model for the given predictions.

    Attributes
    ----------
    predictions : pd.DataFrame
        A DataFrame containing 'Probability_Default' & 'DV' columns.

    PD_column : string
        Name of PD column in the dataframe.

    label_column: string
        Name of the DV column.

    deciles: int
        Number of deciles


    Methods
    -------

    plot_roc_curve(): Plots the ROC Curve
    compute_auc_gini(): Returns the AUC and Gini coefficient
    compute_gains_table_ks(): Computes the gains table from the provided predictions DataFrame. Returns the gains table & KS value from the gains table.
    """

    def __init__(self, predictions_df, PD_column, label_column, deciles=10):
        self.predictions = predictions_df
        self.deciles = deciles
        self.PD_column = PD_column
        self.label_column = label_column

    def compute_gains_table_ks(self):

        self.predictions['Bins'] = pd.qcut(
            self.predictions[self.PD_column], q=self.deciles, duplicates='drop')
        self.predictions['Total'] = 1
        self.predictions.rename(
            columns={self.label_column: 'Bads'}, inplace=True)

        gains_table = self.predictions[['Bins', 'Bads', 'Total']].groupby(
            self.predictions['Bins']).sum()

        gains_table['Goods'] = gains_table['Total'] - gains_table['Bads']
        gains_table['Cumulative_bads'] = gains_table['Bads'].cumsum()
        gains_table['Cumulative_goods'] = gains_table['Goods'].cumsum()
        gains_table['Cumulative_Bad_Rate'] = (
            gains_table['Cumulative_bads'] / gains_table['Cumulative_bads'].max() * 100).round(2)
        gains_table['Cumulative_Good_Rate'] = (
            gains_table['Cumulative_goods'] / gains_table['Cumulative_goods'].max() * 100).round(2)
        gains_table['KS'] = abs(
            gains_table["Cumulative_Bad_Rate"] - gains_table["Cumulative_Good_Rate"])
        gains_table = gains_table[['Bads', 'Goods', 'Total', 'Cumulative_bads',
                                   'Cumulative_goods', 'Cumulative_Bad_Rate', 'Cumulative_Good_Rate', 'KS']]
        model_ks = gains_table['KS'].max()

        def identify_max(series):
            max_value = series.max()
            return ['<---' if i == max_value else '' for i in series]

        def highlight_max(series):
            max_value = series.max()
            return ['background-color: aquamarine' if i == max_value else '' for i in series]

        # Apply the identify_max & highlight_max functions to the DataFrame
        gains_table['Max_KS'] = identify_max(gains_table['KS'])
        gains_table = gains_table.style.apply(highlight_max, subset=['KS'])

        return gains_table, model_ks

    def compute_auc_gini(self):
        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(
            y_score=self.predictions[self.PD_column], y_true=self.predictions[self.label_column])
        gini = 2*auc - 1
        return auc, gini

    def plot_roc_curve(self):
        import matplotlib.pyplot as plt
        from sklearn.metrics import roc_curve, auc
        # Compute FPR, TPR, and thresholds
        fpr, tpr, thresholds = roc_curve(
            y_true=self.predictions[self.label_column], y_score=self.predictions[self.PD_column])
        # Compute AUC
        roc_auc = auc(fpr, tpr)
        # Plot the ROC curve
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (AUC = %0.5f)' % roc_auc)
        # Plotting the diagonal line (random classifier)
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.show()
