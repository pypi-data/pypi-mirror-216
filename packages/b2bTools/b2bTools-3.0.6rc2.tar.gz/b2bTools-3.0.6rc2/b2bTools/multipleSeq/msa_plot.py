#!/usr/local/bin/python
import os
import numpy as np
import re
import sys
import math
import matplotlib.pyplot as plt
import pandas as pd

os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
import matplotlib as mpl
mpl.use("Agg")


#i dont think this is correct? I need  to know if the flags where put
from ..singleSeq import constants

#SELECTED_PROTEIN_LABELS   =  'Syn_WH5701_01905_273568,VIII_1_CK_Syn_RS9917_06430' #'Q8NTX0'

class MsaPlot:
    def __init__(self,predManager):
        self.predManager = predManager


        #set plot titles and tool list for plotting
        dynamine    = constants.TOOL_DYNAMINE
        efoldmine   = constants.TOOL_DYNAMINE
        disomine    = constants.TOOL_DYNAMINE
        agmata      = constants.TOOL_DYNAMINE

        self.prediction_titles = {}
        if dynamine == True:
            self.prediction_titles = {
                'backbone': "DynaMine backbone dynamics",
                'sidechain': "DynaMine sidechain dynamics",
                'ppII': "DynaMine conformational propensities: ppII (polyproline II)",
                'coil': "DynaMine conformational propensities: Coil",
                'sheet': "DynaMine conformational propensities: Sheet",
                'helix': "DynaMine conformational propensities: Helix"}
        if efoldmine == True:
            self.prediction_titles['earlyFolding'] = "Early folding (EFoldMine)"
        if disomine == True:
            self.prediction_titles['disoMine'] = "Disorder (disoMine)"
        if agmata == True:
            self.prediction_titles['agmata'] = "Beta aggregation (AgMata)"

    def occupancy(self):
        msa = self.predManager.ms.seqAlignments
        alignment_df = pd.DataFrame.from_dict(msa, columns=['label','seq'])
        seq_df = pd.DataFrame(alignment_df.seq.apply(list).tolist())

        sequences_count, residues_count = seq_df.shape
        occupancy = 1 - (seq_df == '-').sum() / sequences_count

        return  (sequences_count, residues_count , occupancy) #tupel (INT,INT,LIST)

    def get_selected_protein_data (self, SELECTED_PROTEIN_LABELS):

        pred_dict=self.predManager.ms.allPredictions
        pred_df = pd.DataFrame.from_dict(pred_dict)

        selected_protein_df = pd.DataFrame()
        if SELECTED_PROTEIN_LABELS != []:
            for i in SELECTED_PROTEIN_LABELS:
                sel_df = pred_df.filter(like=i)
                rows,cols = sel_df.shape
                if cols > 1:
                    raise ValueError("Protein identifier is not unique:", i)
                if sel_df.empty:
                    raise ValueError("Selected protein not found in MSA:", i)
                else:
                    # TRY: maybe this if can be deleted
                    if selected_protein_df.empty:
                        selected_protein_df = sel_df
                    else:
                        selected_protein_df=pd.concat([selected_protein_df,sel_df],axis =1)

        return selected_protein_df #dataframe with selected proteins, all predictor results

    def plot_biophysical_msa(self, SELECTED_PROTEIN_LABELS):

        occupancy_tup = self.occupancy()
        selected_proteins_all_pred_df = self.get_selected_protein_data(SELECTED_PROTEIN_LABELS)
        #what happens if SELECTED_PROTEIN_LABELS is nothing?

        stats_dict=self.predManager.ms.alignedPredictionDistribs
        stats_df = pd.DataFrame.from_dict(stats_dict)

        #plot by predictor
        predictions = list(self.prediction_titles.keys())
        for prediction in predictions:
            stats_per_pred_df = pd.DataFrame.from_records(stats_df['results'][prediction])
            self.plot_biophysical_msa_internal(selected_proteins_all_pred_df, occupancy_tup , prediction, stats_per_pred_df)

    def plot_biophysical_msa_internal(self, selected_proteins_all_pred_df, occupancy_tup , prediction, stats_per_pred_df):

        axis_titles = {
            "x": "Residue position in the MSA",
            "y": "Prediction values"}

        sequences_count, residues_count , occupancy = occupancy_tup

        # go in the loop:

        #Plot representation
        fig, (ax1,ax2) = plt.subplots(2,sharex=True, gridspec_kw={'height_ratios': [10, 1]})
        fig.set_figwidth(20)
        fig.set_figheight(10)

        figlabel = 'Predicted biophysical properties of the MSA:\n %s aligned residues from %s sequences ' %(residues_count,sequences_count)
        plt.suptitle(figlabel, fontsize=14)

        col='blue'

        #remove nan values
        df = stats_per_pred_df.dropna(axis=1)

        firstq = df['firstQuartile'].tolist()
        thirdq = df['thirdQuartile'].tolist()
        bottom = df['bottomOutlier'].tolist()
        top = df['topOutlier'].tolist()

        x=np.arange(0,residues_count,1)
        ax1.fill_between(x, firstq, thirdq, alpha=0.3, color=col, label='1st-3rd Quartiles')
        ax1.fill_between(x, bottom, top, alpha=0.1, color=col, label='Outliers')
        ax1.plot(df['median'].tolist(), linewidth=1.25, color=col, label='Median')

        ax2.bar(x, occupancy,  width=1)
        ax1.axis([0,residues_count, min(bottom)-0.05, max(top)+0.05])

        #Add cutoffs for predictions
        if prediction == 'backbone':
            ax1.axhline(y=1.0, color='green', linewidth= 1.5, linestyle='-.', label='Above: Membrane spaning')
            ax1.axhline(y=0.8, color='orange', linewidth= 1.5, linestyle='-.', label='Above: Rigid')
            if min(bottom)-0.05 < 0.69:
                ax1.axhline(y=0.69, color='red', linewidth= 1.5, linestyle='-.', label='Above: Context dependent Below: Flexible')
        if prediction == 'earlyFolding':
            ax1.axhline(y=0.169, color='red', linewidth= 1.5, linestyle='-.', label='Above: Likely to start folding')
        if prediction == 'disoMine':
            ax1.axhline(y=0.5, color='red', linewidth= 1.5, linestyle='-.', label='Above: Likely to be disordered')

        #Add the selected protein if there are some
        colors = ['magenta', 'purple', 'cyan'] #adapt in function of number of proteins of interest, now max 3 can be studied simultanously
        if selected_proteins_all_pred_df.empty == False:
            selected_proteins = selected_proteins_all_pred_df.columns.tolist()
            for sel_protein_label in selected_proteins:
                row = selected_proteins_all_pred_df.loc[prediction, sel_protein_label]
                ax1.plot(row, '-s', linewidth=1.5, color=colors[c], label=f'Prediction {sel_protein_label}')

        #add legend
        plt.figlegend(loc='lower center', ncol =4)
        fig.subplots_adjust(top=0.9, hspace = 0.0001)

        ax1.set_title(self.prediction_titles[prediction])
        ax1.set_ylabel(axis_titles['y'])
        ax2.set_xlabel(axis_titles['x'])
        ax2.set_ylabel('Occupancy')

        return fig
