#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:35:30 2023

The functions in this script are specific to the champions comparison. 

@author: mariohevia
"""


import matplotlib.pyplot as plt
import utils

"""
Gives the data ready to plot from a single Champions experiment.
Used by plotChampions and plotChampionsVSCommon
"""
def getChampions(data, legend_key=None):
    ts = data['t'].unique().tolist()
    data_names = ['min', 'q1', 'median', 'q3', 'max', 'mean']
    data_dict = {'ts':ts}
    for coea in ['coea1', 'coea2']:
        for pop in ['pred', 'prey']:
            for name in data_names:
                key = coea+'_'+pop+'_'+name
                data_dict[key] = [data[data['t'] == i].loc[:, key].median() for i in ts]
    if legend_key!=None:
        alg_1 = data["coea1:"+legend_key].unique().tolist()[0]
        alg_2 = data["coea2:"+legend_key].unique().tolist()[0]
    else:
        alg_1, alg_2 = "coea1", "coea2"
    return alg_1, alg_2, data_dict

"""
Plots the data into one axis from a single algorithm/pop from a Champions experiment.
Used by plotChampions and plotChampionsVSCommon
"""
def plotAxChampions(ax, alg, ts, median, q1, q3):
    ax.plot(ts, median, label=alg)
    ax.fill_between(ts, q1, q3, hatch= '//', alpha = 0.3)
    return ax

"""
Plots the median and interquartiles of a single champions comparison 
(multiple runs) into one plot. 

file_path : string
    Path to the file to plot.
legend_key : string (optional)
    String in the keys of the file to label the two algorithms competing in the 
    form coea#:legend_key. If given the values of this key are used as legends 
    for the lines and the parameter "legends" is ignored.
legends : 2-tuple of strings - (string, string) (optional)
    Strings used as legends for the lines.
fig_size: 2-tuple of floats - (float, float) (optional)
    Size of the figure
title: string (optional)
    Title in the plot.
"""
def plotChampions(file_path, fig_size=(10, 8), title=None, legend_key=None, legends=None, file_name=None):
    if legends==None and legend_key==None:
        raise ValueError('Either legends or legend_key must be assigned.')
    if legend_key==None and (type(legends)!=tuple or type(legends)!=list):
        raise ValueError('legends is expected to be a 2-tuple or a list of strings - (string, string).')
    if legend_key==None and len(legends)!=2:
        raise ValueError('legends is expected to be a 2-tuple or a list of strings - (string, string).')
    if legend_key==None and (type(legends[0])!=str or type(legends[1])!=str):
        raise ValueError('legends is expected to be a 2-tuple or a list of strings - (string, string).')
    data = utils.ocamlFileToPandas(file_path)
    alg_1, alg_2, data_dict = getChampions(data, legend_key)
    fig = plt.figure(figsize=fig_size)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    if legend_key==None:
        alg_1=legends[0]
        alg_2=legends[1]
    ax1 = plotAxChampions(ax1, alg_1, data_dict['ts'], data_dict['coea1_pred_median'],
                                    data_dict['coea1_pred_q1'], data_dict['coea1_pred_q3'])
    ax1 = plotAxChampions(ax1, alg_2, data_dict['ts'], data_dict['coea2_pred_median'],
                                    data_dict['coea2_pred_q1'], data_dict['coea2_pred_q3'])
    
    ax2 = plotAxChampions(ax2, alg_1, data_dict['ts'], data_dict['coea1_prey_median'],
                                    data_dict['coea1_prey_q1'], data_dict['coea1_prey_q3'])
    ax2 = plotAxChampions(ax2, alg_2, data_dict['ts'], data_dict['coea2_prey_median'],
                                    data_dict['coea2_prey_q1'], data_dict['coea2_prey_q3'])
    if title != None:
        ax1.set_title(title)
    ax1.legend()
    ax2.set_xlabel('t')
    ax1.set_ylabel('Payoff in the population (pred)')
    ax2.set_ylabel('Payoff in the population (prey)')
    ax1.set_facecolor("#e6e6e6")
    ax2.set_facecolor("#e6e6e6")
    ax1.get_legend().get_frame().set_facecolor("white")
    if file_name == None:
        plt.show()
    else:
        plt.savefig(file_name, bbox_inches = 'tight')
    plt.clf()
    plt.close()

""" 
TODO: Add explanation.
"""
def addChampionsVSCommon(ax1, ax2, data, legend_key=None, legends=None):
    alg_1, alg_2, data_dict = getChampions(data, legend_key)
    if legend_key==None:
        alg_1=legends
    ax1 = plotAxChampions(ax1, alg_1, data_dict['ts'], data_dict['coea1_pred_median'],
                                    data_dict['coea1_pred_q1'], data_dict['coea1_pred_q3'])
    ax2 = plotAxChampions(ax2, alg_1, data_dict['ts'], data_dict['coea1_prey_median'],
                                    data_dict['coea1_prey_q1'], data_dict['coea1_prey_q3'])
    return ax1, ax2

"""
Plots the median and interquartiles of a several champions comparisons 
(multiple runs) into one plot. 

file_paths : list of strings
    Paths to the files to plot.
legend_key : string (optional)
    String in the keys of the file to label the two algorithms competing in the 
    form coea#:legend_key. If given the values of this key are used as legends 
    for the lines and the parameter "legends" is ignored.
legends : list of strings
fig_size: 2-tuple of floats - (float, float) (optional)
    Size of the figure
title: string (optional)
    Title in the plot.
xlims: 2-tuple of floats - (float, float) (optional)
    Limits in the x axis.
ylims: 2-tuple of floats - (float, float) (optional)
    Limits in the y axis.
"""
def plotChampionsVSCommon(file_paths, fig_size=(10, 8), title=None, legend_key=None, legends=None, file_name=None, xlims=None, ylims=None):
    if legends==None and legend_key==None:
        raise ValueError('Either legends or legend_key must be assigned.')
    fig = plt.figure(figsize=fig_size)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    for i, path in enumerate(file_paths):
        data = utils.ocamlFileToPandas(path)
        ax1, ax2 = addChampionsVSCommon(ax1, ax2, data=data, filter_dict={}, legend_key=legend_key, legends=legends[i])
    if title!=None:
        ax1.set_title(title)
    if xlims!=None:
        ax1.set_xlim(xlims[0])
        ax2.set_xlim(xlims[1])
    if ylims!=None:
        ax1.set_ylim(ylims[0])
        ax2.set_ylim(ylims[1])
    ax1.legend()
    ax2.set_xlabel('t')
    ax1.set_ylabel('Payoff in the population (pred)')
    ax2.set_ylabel('Payoff in the population (prey)')
    ax1.set_facecolor("#e6e6e6")
    ax2.set_facecolor("#e6e6e6")
    ax1.get_legend().get_frame().set_facecolor("white")
    if file_name == None:
       plt.show()
    else:
       plt.savefig(file_name, bbox_inches = 'tight')
    plt.clf()
    plt.close()