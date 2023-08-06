#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 13:41:29 2023

@author: mariohevia

Utility functions to quickly process ocaml output files.

"""

import pandas as pd
import numpy as np
import os
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from io import StringIO
import itertools
from PyPDF2 import PdfMerger
import networkx as nx

"""
Sets the parameters asked by GECCO for matplotlib and changes the colours to colorblind.
"""
def setGeccoRules():
    sns.set()
    sns.color_palette("colorblind")
    # Parameters for GECCO paper
    matplotlib.rcParams['pdf.fonttype'] = 42
    matplotlib.rcParams['ps.fonttype'] = 42
    plt.rcParams.update({'font.size': 14})

"""
Gets all files ending with that include the string ext within the given path.
"""
def getPaths(data_path = '.', ext=".out"):
    filepaths = []
    for subdir, dirs, files in os.walk(data_path):
        for file in files:
            filepaths.append(os.path.join(subdir, file))
    filepaths.sort()
    return [i for i in filepaths if ext in i]

'''
Merges all pdfs inside the path into one (deletes the file where it will write).
'''
def MergePDFs(path, title):
    if title[-4:]!=".pdf":
        title=title+".pdf"
    # Removes any pdf with the same name as the output pdf
    if os.path.isfile(path+title):
        os.remove(path+title) 
    # Reads all the files with ".pdf" from the path
    pdfs = getPaths(path, ext=".pdf")
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(path+title)
    merger.close()
    
"""
Transforms an ocaml file into a pandas DataFrame 
(assumes that the headers will have "t" as first variable name).
"""
def ocamlFileToPandas(filepath):
    with open(filepath, 'r') as f:
        current_file = f.readlines()
        i = 0
        headers = current_file[i].split()
        while headers[0] != "t":
            i += 1
            headers = current_file[i].split()
        current_file = [line for line in current_file if line[0] != "t"]
        current_file = "\n".join(current_file)
        data = pd.read_csv(StringIO(current_file), delimiter="\t", names=headers)
        return data  
"""
Filters a DataFrame with all the key, values from filter_dict.
"""
def filterData(data, filter_dict):
    # Filters the data
    for key, value in filter_dict.items():
        data = data[data[key] == value]
    return data
    
"""
TODO
Gives runtime statistics with only the data with filter_dict. 
Outputs only rows that have all columns (key) with the value in filter_dict.
"""
def getRuntimeWithFilter(data, filter_dict):
    # Filters the data
    data = filterData(data, filter_dict)
    return 0


    
def getStatisticsHammingDistances(filepath):
    with open(filepath, 'r') as f:
        current_file = f.readlines()
        fevals = []
        mean_pred = []
        median_pred = []
        stdev_pred = []
        mean_prey = []
        median_prey = []
        stdev_prey = []
        for i, line in enumerate(current_file):
            modulo = i%3
            if modulo==0:
                fevals.append(int(line.split()[-1]))
            elif modulo==1:
                pred_dists=[float(dist.split("-")[0]) for dist in line.strip().split("\t")]
                # pred_dists=[float(dist) for dist in line.split()]
                mean_pred.append(statistics.mean(pred_dists))
                median_pred.append(statistics.median(pred_dists))
                stdev_pred.append(statistics.stdev(pred_dists))
            else:
                prey_dists=[float(dist.split("-")[0]) for dist in line.strip().split("\t")]
                # prey_dists=[float(dist) for dist in line.split()]
                mean_prey.append(statistics.mean(prey_dists))
                median_prey.append(statistics.median(prey_dists))
                stdev_prey.append(statistics.stdev(prey_dists))
        processed_file = {"fevals":fevals,"mean_pred":mean_pred,
                          "median_pred":median_pred,"stdev_pred":stdev_pred,
                          "mean_prey":mean_prey,"median_prey":median_prey,
                          "stdev_prey":stdev_prey, 
                           "experiment_name":[filepath.split("/")[-3].split("-")[0][10:-5] for i in range(len(fevals))]}
                          # "experiment_name":[filepath.split("/")[-1][:-4] for i in range(len(fevals))]}
        return pd.DataFrame(processed_file)
    
def plotStatisticsHammingDistances(file_paths, fig_size=(10, 16), legend_replacements=[("","")], title=None, legends=None, file_name=None):
    fig = plt.figure(figsize=fig_size)
    ax1 = fig.add_subplot(411)
    ax2 = fig.add_subplot(412)
    ax3 = fig.add_subplot(413)
    ax4 = fig.add_subplot(414)
    data = []
    for i, path in enumerate(file_paths):
        data.append(getStatisticsHammingDistances(path))
    data = pd.concat(data, axis=0, ignore_index=True)
    for old,new in legend_replacements:
        data["experiment_name"] = data["experiment_name"].str.replace(old, new)
    # print(data[data['fevals'] == 0].shape)
    sns.lineplot(ax=ax1, data=data, x="fevals", y="median_pred", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)), )
    sns.lineplot(ax=ax2, data=data, x="fevals", y="median_prey", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)),legend=False)
    sns.lineplot(ax=ax3, data=data, x="fevals", y="stdev_pred", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)),legend=False)
    sns.lineplot(ax=ax4, data=data, x="fevals", y="stdev_prey", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)),legend=False)
    if title!=None:
        ax1.set_title(title)
    ax1.legend(title="")
    ax1.set_ylabel('Median (pred)')
    ax2.set_ylabel('Median (prey)')
    ax3.set_ylabel('Std. dev. (pred)')
    ax4.set_ylabel('Std. dev. (prey)')
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax3.set_xlabel('')
    ax4.set_xlabel('t')
    ax1.set_facecolor("#e6e6e6")
    ax2.set_facecolor("#e6e6e6")
    ax3.set_facecolor("#e6e6e6")
    ax4.set_facecolor("#e6e6e6")
    ax1.get_legend().get_frame().set_facecolor("white")
    if file_name == None:
       plt.show()
    else:
       plt.savefig(file_name, bbox_inches = 'tight')
    plt.clf()
    plt.close()
    
def getStatisticsPayoffs(filepath):
    with open(filepath, 'r') as f:
        current_file = f.readlines()
        fevals = []
        mean_pred = []
        median_pred = []
        stdev_pred = []
        mean_prey = []
        median_prey = []
        stdev_prey = []
        for i, line in enumerate(current_file):
            modulo = i%2
            if modulo==0:
                fevals.append(int(line.split()[-1]))
            elif modulo==1:
                payoffs=[(float(payoff.split(',')[0][1:]),float(payoff.split(',')[1][:-1])) for payoff in line.split()]
                payoffs=[list(t) for t in zip(*payoffs)]
                pred_payoffs=payoffs[0]
                mean_pred.append(statistics.mean(pred_payoffs))
                median_pred.append(statistics.median(pred_payoffs))
                stdev_pred.append(statistics.stdev(pred_payoffs))
                prey_payoffs=payoffs[1]
                mean_prey.append(statistics.mean(prey_payoffs))
                median_prey.append(statistics.median(prey_payoffs))
                stdev_prey.append(statistics.stdev(prey_payoffs))
        processed_file = {"fevals":fevals,"mean_pred":mean_pred,
                          "median_pred":median_pred,"stdev_pred":stdev_pred,
                          "mean_prey":mean_prey,"median_prey":median_prey,
                          "stdev_prey":stdev_prey, 
                          "experiment_name":[filepath.split("/")[-1][:-4] for i in range(len(fevals))]}
        return pd.DataFrame(processed_file)
    
def plotStatisticsPayoffs(file_paths, fig_size=(10, 8), legend_replacements=[("","")], title=None, legends=None, file_name=None):
    fig = plt.figure(figsize=fig_size)
    # ax1 = fig.add_subplot(411)
    # ax2 = fig.add_subplot(412)
    # ax3 = fig.add_subplot(413)
    # ax4 = fig.add_subplot(414)
    ax3 = fig.add_subplot(211)
    ax4 = fig.add_subplot(212)
    data = []
    for i, path in enumerate(file_paths):
        data.append(getStatisticsPayoffs(path))
    data = pd.concat(data, axis=0, ignore_index=True)
    for old,new in legend_replacements:
        data["experiment_name"] = data["experiment_name"].str.replace(old, new)
    # print(data[data['fevals'] == 0].shape)
    # sns.lineplot(ax=ax1, data=data, x="fevals", y="median_pred", hue="alg", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)), )
    # sns.lineplot(ax=ax2, data=data, x="fevals", y="median_prey", hue="alg", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)),legend=False)
    sns.lineplot(ax=ax3, data=data, x="fevals", y="stdev_pred", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)))
    sns.lineplot(ax=ax4, data=data, x="fevals", y="stdev_prey", hue="experiment_name", estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)),legend=False)
    if title!=None:
        # ax1.set_title(title)
        ax3.set_title(title)
    # ax1.legend()
    ax3.legend()
    # ax1.set_ylabel('Median (pred)')
    # ax2.set_ylabel('Median (prey)')
    ax3.set_ylabel('Payoff Std. dev. (pred)')
    ax4.set_ylabel('Payoff Std. dev. (prey)')
    # ax1.set_xlabel('')
    # ax2.set_xlabel('')
    ax3.set_xlabel('')
    ax4.set_xlabel('t')
    # ax1.set_facecolor("#e6e6e6")
    # ax2.set_facecolor("#e6e6e6")
    ax3.set_facecolor("#e6e6e6")
    ax4.set_facecolor("#e6e6e6")
    # ax1.get_legend().get_frame().set_facecolor("white")
    ax3.get_legend().get_frame().set_facecolor("white")
    if file_name == None:
       plt.show()
    else:
       plt.savefig(file_name, bbox_inches = 'tight')
    plt.clf()
    plt.close()
    
############### DELETE THIS!! #############
# def mad(x):
#     return (x[1]-x[0])/(0.1)
############### DELETE THIS!! #############
    
def plotRuntimeGroupByExperimentChi(file_paths, fig_size=(10, 6), legend_replacements=[("","")], title=None, legends=None, file_name=None, hue="experiment_name"):
    fig = plt.figure(figsize=fig_size)
    ax1 = fig.add_subplot(111)
    data = []
    for path in file_paths:
        data.append(ocamlFileToPandas(path))
    data = pd.concat(data, axis=0, ignore_index=True)
    if hue!="experiment_name":
        data["experiment_name"] = data["experiment_name"]+ '_' +data[hue].astype(str)
    for old,new in legend_replacements:
        data["experiment_name"] = data["experiment_name"].str.replace(old, new)
    
    ############### DELETE THIS!! #############
    
    # for i in data["experiment_name"].unique():
    #     filtered = data[data['experiment_name'] == i]
    #     medians = filtered.groupby(['chi_prey','experiment_name'])['t'].median()
    #     medians_min = medians.min()
    #     threshold = medians.min()+160000
    #     filtered = medians.loc[lambda x : x == medians_min].index[0][0]
    #     filtered2 = medians[((medians.index > (float(filtered),medians.index[0][1])) & (medians > threshold))].index[0][0]
    #     # filtered2 = medians.loc[lambda x : x >= threshold].filter(items=[i/10 for i in range(50) if i/10>filtered], axis=0)
    #     window = medians.rolling(window=2).apply(mad, raw=True).dropna()
    #     window1 = window.loc[lambda x : x >= 75000].index[0][0]
    #     window2 = window.loc[lambda x : x >= 100000].index[0][0]
    #     print(i, medians_min, '\nmin chi: ', filtered, '\nchi above threshold: ', filtered2, '\nchi above slope:', window1, window2)
    #     print("~~~~~~~~~~~~~~~~~")
    ############### DELETE THIS!! #############
    
    # palette = sns.color_palette("hls", 6) 
    # all_colours = palette+palette[:-1]
    
    hue_order = data['experiment_name'].unique().tolist()
    hue_order.sort()
    all_colours = sns.color_palette("hls", len(hue_order))
    data.rename(columns = {'chi_prey':r'mutation parameter $\chi$'}, inplace = True)
    sns.lineplot(ax=ax1, data=data, x=r'mutation parameter $\chi$', y="t", hue="experiment_name", linewidth=1, estimator=np.median, errorbar=lambda x: (np.quantile(x, 0.25), np.quantile(x, 0.75)), palette=all_colours, hue_order=hue_order)
    
    # Changes the linestyles of the plot, first inside the plot and later inside the legend
    all_linestyles = ['-', '-', '-', '-','-','--','--','--','--','--','--']
    # all_linestyles = ['-', ':', '--', '-.',(5, (10, 3)), (0, (5, 8))]
    for line, ls in zip(ax1.get_lines(), itertools.cycle(all_linestyles)):
        line.set_linestyle(ls)
    for line, ls in zip(ax1.get_legend_handles_labels()[0], itertools.cycle(all_linestyles)):
        line.set_linestyle(ls)
        
    ax1.set_facecolor("#e6e6e6")
    ax1.legend(bbox_to_anchor=(1, 1), loc="upper left")
    ax1.get_legend().get_frame().set_facecolor("white")
    
    if title!=None:
        ax1.set_title(title)
    if file_name == None:
       plt.show()
    else:
       plt.savefig(file_name, bbox_inches = 'tight')
    plt.clf()
    plt.close()

def getHammingvsPathDistance(filepath, shortest_paths_lens, infinite_path_len):
    with open(filepath, 'r') as f:
        current_file = f.readlines()
        fevals = []
        pred_dists = []
        pred_path_lens = []
        prey_dists = []
        prey_path_lens = []
        for i, line in enumerate(current_file):
            modulo = i%3
            if modulo==0:
                fevals_temp = int(line.split()[-1])
            elif modulo==1:
                temp=[(float(dist.split("-")[0]), eval(dist.split("-")[1])) for dist in line.strip().split("\t")[:-1]]
                pred_dists.extend([i for (i, (j, k)) in temp])
                fevals.extend([fevals_temp for i in temp])
                for (i, (j, k)) in temp:
                    try:
                        pred_path_lens.append(shortest_paths_lens[str(j)][str(k)])
                    except:
                        pred_path_lens.append(infinite_path_len)
            else:
                temp=[(float(dist.split("-")[0]), eval(dist.split("-")[1])) for dist in line.strip().split("\t")[:-1]]
                prey_dists.extend([i for (i, (j, k)) in temp])
                for (i, (j, k)) in temp:
                    try:
                        prey_path_lens.append(shortest_paths_lens[str(j)][str(k)])
                    except:
                        prey_path_lens.append(infinite_path_len)
        processed_file = {"fevals":fevals,"pred_dists":pred_dists, "pred_path_lens":pred_path_lens,
                          "prey_dists":prey_dists, "prey_path_lens":prey_path_lens,
                          "experiment_name":[filepath.split("/")[-1][:-4] for i in range(len(fevals))]}
                          # "experiment_name":[filepath.split("/")[-3].split("-")[0][10:-5] for i in range(len(fevals))]}
        return pd.DataFrame(processed_file)

def plotHammingvsPathDistance(file_path, graph_path, fig_size=(10, 12), legend_replacements=[("","")], title=None, legends=None, file_name=None, only_last_gen=True, verbose=False, xlims=None, ylims=None, remove_all_legends=False, evals_per_gen=1):
    graph = nx.nx_pydot.read_dot(graph_path)
    shortest_paths_lens =  dict(nx.shortest_path_length(graph))
    if nx.is_directed(graph) and verbose:
        in_degree_sequence = sorted((d for n, d in graph.in_degree()), reverse=True)
        out_degree_sequence = sorted((d for n, d in graph.out_degree()), reverse=True)
        print(graph_path.split("/")[-1])
        print("Minimum:", min(in_degree_sequence), min(out_degree_sequence))
        print("Median:", statistics.median(in_degree_sequence), statistics.median(out_degree_sequence))
        print("Mean:", statistics.mean(in_degree_sequence), statistics.mean(out_degree_sequence))
        print("Maximum:", max(in_degree_sequence), max(out_degree_sequence))
    elif verbose:
        degree_sequence = sorted((d for n, d in graph.degree()), reverse=True)
        print(graph_path.split("/")[-1])
        print("Minimum:", min(degree_sequence))
        print("Median:", statistics.median(degree_sequence))
        print("Mean:", statistics.mean(degree_sequence))
        print("Maximum:", max(degree_sequence))
    max_path_len = max([max(i.values()) for i in shortest_paths_lens.values()])
    # data.append(getHammingvsPathDistance(file_path,shortest_paths_lens,20+nx.number_of_nodes(graph)))
    data = getHammingvsPathDistance(file_path,shortest_paths_lens,round(1.2*max_path_len))
    for old,new in legend_replacements:
        data["experiment_name"] = data["experiment_name"].str.replace(old, new)
    if only_last_gen==None:
        max_evals = data['fevals'].max()
        data = data[data['fevals'] == max_evals]
    all_evals = data['fevals'].unique().tolist()
    all_evals.sort()
    for i, j in enumerate(all_evals):
        fig = plt.figure(figsize=fig_size)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        temp_data = data[data['fevals'] == j]
        sns.scatterplot(ax=ax1, data=temp_data, y="pred_dists", x="pred_path_lens", hue="experiment_name", markers='.')
        sns.scatterplot(ax=ax2, data=temp_data, y="prey_dists", x="prey_path_lens", hue="experiment_name", markers='.')
        if title!=None:
            ax1.set_title(title+" (gen "+str(round(j/evals_per_gen))+")")
        if xlims!=None:
            ax1.set_xlim(xlims[0])
            ax2.set_xlim(xlims[1])
        if ylims!=None:
            ax1.set_ylim(ylims[0])
            ax2.set_ylim(ylims[1])
        if remove_all_legends:
            ax1.get_legend().remove()
        else:
            ax1.get_legend().get_frame().set_facecolor("white")
        ax2.get_legend().remove()
        ax1.set_xlabel('Path length (pred)')
        ax2.set_xlabel('Path length (prey)')
        ax1.set_ylabel('Hamming distance')
        ax2.set_ylabel('Hamming distance')
        ax1.set_facecolor("#e6e6e6")
        ax2.set_facecolor("#e6e6e6")
        if file_name == None:
            plt.show()
        else:
            plt.savefig(file_name+"_"+str(i), bbox_inches = 'tight', dpi=300)
        plt.clf()
        plt.close()


def getPayoffsvsPathDistance(filepath, shortest_paths_lens, infinite_path_len):
    with open(filepath, 'r') as f:
        current_file = f.readlines()
        fevals = []
        pred_payoffs = []
        pred_path_lens = []
        prey_payoffs = []
        prey_path_lens = []
        for i, line in enumerate(current_file):
            modulo = i%2
            if modulo==0:
                fevals_temp = int(line.split()[-1])
            elif modulo==1:
                temp=[(eval(dist.split(" ")[0]), eval(dist.split(" ")[1])) for dist in line.strip().split("\t")[:-1]]
                pred_payoffs.extend([i for ((i, _), (_, _)) in temp])
                prey_payoffs.extend([j for ((_, j), (_, _)) in temp])
                fevals.extend([fevals_temp for i in temp])
                for (_, (k, l)) in temp:
                    try:
                        short_path = shortest_paths_lens[str(k)][str(l)]
                        pred_path_lens.append(short_path)
                        prey_path_lens.append(short_path)
                    except:
                        pred_path_lens.append(infinite_path_len)
                        prey_path_lens.append(infinite_path_len)
        processed_file = {"fevals":fevals,"pred_payoffs":pred_payoffs, "pred_path_lens":pred_path_lens,
                          "prey_payoffs":prey_payoffs, "prey_path_lens":prey_path_lens,
                          "experiment_name":[filepath.split("/")[-1][:-4] for i in range(len(fevals))]}
                          # "experiment_name":[filepath.split("/")[-3].split("-")[0][10:-5] for i in range(len(fevals))]}
        return pd.DataFrame(processed_file)

def plotPayoffsvsPathDistance(file_path, graph_path, fig_size=(10, 12), legend_replacements=[("","")], title=None, legends=None, file_name=None, only_last_gen=True, verbose=False, xlims=None, ylims=None, remove_all_legends=False, evals_per_gen=1):
    graph = nx.nx_pydot.read_dot(graph_path)
    shortest_paths_lens =  dict(nx.shortest_path_length(graph))
    if nx.is_directed(graph) and verbose:
        in_degree_sequence = sorted((d for n, d in graph.in_degree()), reverse=True)
        out_degree_sequence = sorted((d for n, d in graph.out_degree()), reverse=True)
        print(graph_path.split("/")[-1])
        print("Minimum:", min(in_degree_sequence), min(out_degree_sequence))
        print("Median:", statistics.median(in_degree_sequence), statistics.median(out_degree_sequence))
        print("Mean:", statistics.mean(in_degree_sequence), statistics.mean(out_degree_sequence))
        print("Maximum:", max(in_degree_sequence), max(out_degree_sequence))
    elif verbose:
        degree_sequence = sorted((d for n, d in graph.degree()), reverse=True)
        print(graph_path.split("/")[-1])
        print("Minimum:", min(degree_sequence))
        print("Median:", statistics.median(degree_sequence))
        print("Mean:", statistics.mean(degree_sequence))
        print("Maximum:", max(degree_sequence))
    max_path_len = max([max(i.values()) for i in shortest_paths_lens.values()])
    data = getPayoffsvsPathDistance(file_path,shortest_paths_lens,round(1.2*max_path_len))
    for old,new in legend_replacements:
        data["experiment_name"] = data["experiment_name"].str.replace(old, new)
    if only_last_gen==None:
        max_evals = data['fevals'].max()
        data = data[data['fevals'] == max_evals]
    all_evals = data['fevals'].unique().tolist()
    all_evals.sort()
    
    print(data['pred_payoffs'].min(), data['pred_payoffs'].max())
    print(data['prey_payoffs'].min(), data['prey_payoffs'].max())
    
    for i, j in enumerate(all_evals):
        fig = plt.figure(figsize=fig_size)
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        temp_data = data[data['fevals'] == j]
        sns.scatterplot(ax=ax1, data=temp_data, y="pred_payoffs", x="pred_path_lens", hue="experiment_name", markers='.')
        sns.scatterplot(ax=ax2, data=temp_data, y="prey_payoffs", x="prey_path_lens", hue="experiment_name", markers='.')
        if title!=None:
            ax1.set_title(title+" (gen "+str(round(j/evals_per_gen))+")")
        if xlims!=None:
            ax1.set_xlim(xlims[0])
            ax2.set_xlim(xlims[1])
        if ylims!=None:
            ax1.set_ylim(ylims[0])
            ax2.set_ylim(ylims[1])
        if remove_all_legends:
            ax1.get_legend().remove()
        else:
            ax1.get_legend().get_frame().set_facecolor("white")
        ax2.get_legend().remove()
        ax1.set_xlabel('Path length (pred)')
        ax2.set_xlabel('Path length (prey)')
        ax1.set_ylabel('Payoff (pred)')
        ax2.set_ylabel('Payoff (prey)')
        ax1.set_facecolor("#e6e6e6")
        ax2.set_facecolor("#e6e6e6")
        if file_name == None:
            plt.show()
        else:
            plt.savefig(file_name+"_"+str(i), bbox_inches = 'tight', dpi=300)
        plt.clf()
        plt.close()


# if __name__ == "__main__":
#     setGeccoRules()
#     experiment_path = "/home/mariohevia/Documents/University/Coevolution/FlipIt/SDCoEA vs PDCoEA/"
#     paths = getPaths(experiment_path)
    
#     for path in paths:
#         title=path.split('/')[-1][:-4]
#         plotChampionsWithFilter(file_path=path, title=title, legends=("SD-CoEA","PD-CoEA"), file_name=experiment_path+title+".pdf")
    
#     experiment_path = "/home/mariohevia/Documents/University/Coevolution/FlipIt/Experiments/"
#     home_path = experiment_path+"gos/"
#     output_path = home_path+"Plots/"
#     paths = getPaths(home_path+"Payoffs/old_Payoffs3/Payoffs_directed/")
#     pretty_titles = {"chain_2":"1D-graph","doughnut_2":"2D-graph", "erdos_2":"Erdös-Rényi", "barabasi_2":"Barabási-Albert",
#                       "erdos_d":"Erdös-Rényi (double)","pdcoea_p":"PDCoEA vs PDCoEA",
#                       "chain_p":"1D-graph vs PDCoEA","doughnut_p":"2D-graph vs PDCoEA", "erdos_p":"Erdös-Rényi vs PDCoEA", "barabasi_p":"Barabási-Albert vs PDCoEA",
#                       "tree_2":"Binary tree", "tree_p":"Binary tree vs PDCoEA"}
    
#     def transform(title, pretty_titles):
#         for k, v in pretty_titles.items():
#             if k in title:
#                 title=v
#         return title
    

    # print("### GOS ###")
    # print("Creating 1 vs 1 comparisons")
    # for path in paths:
    #     title=transform(path, pretty_titles)
    #     if "PDCoEA" not in title:
    #         plotChampionsWithFilter(file_path=path, title=title, legends=("Undirected","Directed"), file_name=output_path+title+".pdf")
    
    
    # print("Creating all vs PDCoEA comparisons")
    # paths = [path for path in paths if "pdcoea" in path] 
    # legends = [transform(path, pretty_titles)[:-10] for path in paths]
    # title = "Comparison (directed)"
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+".pdf")
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+" zoom.pdf", xlims=((40000000, 50000000),(40000000, 50000000)), ylims=((-2,-1),(-2,-1)))
    
    # paths = getPaths(home_path+"Payoffs/old_Payoffs3/Payoffs_undirected/")
    # paths = [path for path in paths if "pdcoea" in path]
    # legends = [transform(path, pretty_titles)[:-10] for path in paths]
    # title = "Comparison (undirected)"
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+".pdf")
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+" zoom.pdf", xlims=((40000000, 50000000),(40000000, 50000000)), ylims=((-2,-1),(-2,-1)))
    
    # print("Creating Hamming distance plots")  
    # legend_replacements=[("_undir",""),("_dir",""),("pdcoea","PDCoEA"),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree"),("gos_distance_","")]
    # paths = getPaths(home_path+"Hamming/Random/")
    # # paths = getPaths(home_path+"Hamming/old_results/")
    # paths = [path for path in paths if "_undir" not in path]
    # title="Diversity Hamming distance (directed)"
    # plotStatisticsHammingDistances(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # paths = getPaths(home_path+"Hamming/Random/")
    # # paths = getPaths(home_path+"Hamming/old_results/")
    # paths = [path for path in paths if "_dir" not in path]
    # title="Diversity Hamming distance (undirected)"
    # plotStatisticsHammingDistances(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # graph_paths = getPaths(home_path+"Hamming/Snapshot/", ext='.dot')
    # paths = getPaths(home_path+"Hamming/Snapshot/")
    # print("Creating Hamming distance plots")  
    # legend_replacements=[("undir_","undir. "),("dir_","dir. "),("pdcoea","PDCoEA"),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree"),("gos_distance_cart_","")]
    # for path, graph_path in zip(paths, graph_paths):
    #     # print(path, graph_path)
    #     plotHammingvsPathDistance([path], [graph_path], legend_replacements=legend_replacements, file_name=output_path+path.split("/")[-1][:-4])
    
    # graph_paths = getPaths(home_path+"Hamming/Videos/", ext='.dot')
    # paths = getPaths(home_path+"Hamming/Videos/")
    # print("Creating Hamming distance videos")  
    # legend_replacements=[("undir_","undir. "),("dir_","dir. "),("pdcoea","PDCoEA"),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree"),("gos_distance_cart_","")]
    # all_ylims=[(0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225),
    #            (0,225)][8:]
    # titles=["Dir. Barabási-Albert",
    #         "Dir. 1-D graph",
    #         "Dir. 2-D graph",
    #         "Dir. Erdos-Rényi",
    #         "Dir. Binary tree",
    #         "Undir. Barabási-Albert",
    #         "Undir. 1-D graph",
    #         "Undir. 2-D graph",
    #         "Undir. Erdos-Rényi",
    #         "Undir. Binary tree"][8:]
    # for k, (path, graph_path) in enumerate(zip(paths[8:], graph_paths[8:])):
    #     print(titles[k])
    #     plotHammingvsPathDistance(path, graph_path, evals_per_gen=625,
    #                               legend_replacements=legend_replacements, ylims=(all_ylims[k], all_ylims[k]), 
    #                               remove_all_legends=True, title=titles[k], 
    #                               file_name=home_path+"Videos/distance_pngs/"+path.split("/")[-1][:-4])
    
    # graph_paths = getPaths(home_path+"Payoffs/Videos/", ext='.dot')
    # paths = getPaths(home_path+"Payoffs/Videos/")
    # print("Creating Payoff videos")  
    # legend_replacements=[("undir_","undir. "),("dir_","dir. "),("pdcoea","PDCoEA"),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree"),("gos_payoff_cart_","")]
    # all_ylims=[(-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3),
    #            (-3,3)][7:]
    # titles=["Dir. Barabási-Albert",
    #         "Dir. 1-D graph",
    #         "Dir. 2-D graph",
    #         "Dir. Erdos-Rényi",
    #         "Dir. Binary tree",
    #         "Undir. Barabási-Albert",
    #         "Undir. 1-D graph",
    #         "Undir. 2-D graph",
    #         "Undir. Erdos-Rényi",
    #         "Undir. Binary tree"][7:]
    # for k, (path, graph_path) in enumerate(zip(paths[7:], graph_paths[7:])):
    #     print(titles[k])
    #     plotPayoffsvsPathDistance(path, graph_path, evals_per_gen=625,
    #                               legend_replacements=legend_replacements, ylims=(all_ylims[k], all_ylims[k]), 
    #                               remove_all_legends=True, title=titles[k], 
    #                               file_name=home_path+"Videos/payoff_pngs/"+path.split("/")[-1][:-4])
    
    
    # print("Creating Diversity_payoffs plots")
    # legend_replacements=[("_undir",""),("_dir",""),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("bin_tree","Binary tree")]
    # paths = getPaths(home_path+"Diversity/old_results/")
    # paths = [path for path in paths if "undir.out" not in path]
    # title="Diversity payoffs (directed)"
    # plotStatisticsPayoffs(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # paths = getPaths(home_path+"Diversity/old_results/")
    # paths = [path for path in paths if "_dir.out" not in path]
    # title="Diversity payoffs (undirected)"
    # plotStatisticsPayoffs(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # MergePDFs(output_path, "GOS_all_results")
    
    # # ######################################################################## 
    # # ######################################################################## 
    # # ######################################################################## 
    
    # home_path = experiment_path+"dir_vs_undir/"
    # output_path = home_path+"Plots/"
    # paths = getPaths(home_path+"Payoffs/old_Payoffs3/Payoffs_directed/")
    
    # print("### DefendIt ###")
    # print("Creating 1 vs 1 comparisons")
    # for path in paths:
    #     title=transform(path, pretty_titles)
    #     if "PDCoEA" not in title:
    #         plotChampionsWithFilter(file_path=path, title=title, legends=("Undirected","Directed"), file_name=output_path+title+".pdf")
    
    # print("Creating all vs PDCoEA comparisons")
    # paths = [path for path in paths if "pdcoea" in path] 
    # legends = [transform(path, pretty_titles)[:-10] for path in paths]
    # title = "Comparison (directed)"
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+".pdf")
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+" zoom.pdf", xlims=((40000000, 50000000),(40000000, 50000000)), ylims=((-100,25000),(-100,20000)))
    
    # paths = getPaths(home_path+"Payoffs/old_Payoffs3/Payoffs_undirected/")
    # paths = [path for path in paths if "pdcoea" in path]
    # legends = [transform(path, pretty_titles)[:-10] for path in paths]
    # title = "Comparison (undirected)"
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+".pdf")
    # plotChampionsVSCommonWithFilter(file_paths=paths, title=title, legends=legends, file_name=output_path+title+" zoom.pdf", xlims=((40000000, 50000000),(40000000, 50000000)), ylims=((15000,24000),(11000,19000)))
    
    # print("Creating Hamming distance plots")
    # legend_replacements=[("_undir",""),("_dir",""),("pdcoea","PDCoEA"),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree"),("binaryflipit_distance_","")]
    # paths = getPaths(home_path+"Hamming/Random/")
    # # paths = getPaths(home_path+"Hamming/old_results/")
    # # paths = [path for path in paths if "_undir." not in path]
    # paths = [path for path in paths if "_undir_" not in path]
    # title="Diversity Hamming distance (directed)"
    # plotStatisticsHammingDistances(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # paths = getPaths(home_path+"Hamming/Random/")
    # # paths = getPaths(home_path+"Hamming/old_results/")
    # # paths = [path for path in paths if "_dir." not in path]
    # paths = [path for path in paths if "_dir_" not in path]
    # title="Diversity Hamming distance (undirected)"
    # plotStatisticsHammingDistances(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")

    # # for path, graph_path in zip(paths, graph_paths):
    # #     # print(path, graph_path)
    # #     plotHammingvsPathDistance([path], [graph_path])

    # print("Creating Diversity_payoffs plots")
    # legend_replacements=[("_undir",""),("_dir",""),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("bin_tree","Binary tree")]
    # paths = getPaths(home_path+"Diversity/old_results/")
    # paths = [path for path in paths if "undir.out" not in path]
    # title="Diversity payoffs (directed)"
    # plotStatisticsPayoffs(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # paths = getPaths(home_path+"Diversity/old_results/")
    # paths = [path for path in paths if "_dir.out" not in path]
    # title="Diversity payoffs (undirected)"
    # plotStatisticsPayoffs(paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")
    
    # MergePDFs(output_path, "DefendIt_all_results")
    
    # print("### Error Threshold ###")
    # home_path = experiment_path+"error_threshold/detailed_results/"
    # output_path = experiment_path+"error_threshold/Plots/"
    # paths = getPaths(home_path)
    # title="Error thresholds"
    # legend_replacements=[("error_",""),("undir_","undir. "),("dir_","dir. "),
    #                       ("barabasi","Barabási-Albert"),("chain", "1D-graph"),
    #                       ("doughnut", "2D-graph"),("erdos","Erdos-Rényi"),
    #                       ("tree","Binary tree")]
    # plotRuntimeGroupByExperimentChi(file_paths=paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf")

    # print("### Erdos Renyi Error Threshold ###")
    # home_path = experiment_path+"error_threshold/erdos_p_results/"
    # output_path = experiment_path+"error_threshold/Plots/"
    # paths = getPaths(home_path)
    # title="Error thresholds (undir. Erdos-Rényi)"
    # legend_replacements=[("error_",""),("undir_",""),("erdos",""),
    #                       ("_varying_p_"," p "),("_nan","")]
    # plotRuntimeGroupByExperimentChi(file_paths=paths, legend_replacements=legend_replacements, title=title, file_name=output_path+title+".pdf", hue="er_p")






#