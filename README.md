# Selecting Alternates for Citizens’ Assemblies
This github repository contains the code for the paper ["Alternates, Assemble! Selecting Optimal Alternates for Citizens’ Assemblies"](https://procaccia.info/wp-content/uploads/2025/02/alternate.pdf) by Angelos Assos, Carmel Baharav, Bailey Flanigan, and Ariel Procaccia. 

The data of the real citizens' assembly instances used to construct the plots in the paper is withheld for privacy reasons.

## A Tour of the Code
Here are some of the important files in this repository:
* __main.py__: This contains all of the different tests that we run in the paper (robustness tests, evaluation on real dropout sets, evaluation on simulated dropout sets, convergence tests, etc). At the very bottom of the file, there are commented out examples of how to call the different functions in the file.
* __data_objects.py__: This contains two different classes -- _Instance_ and _BetaLearner_. The _Instance_ class stores a citizens' assembly instance, and has the functionality for all of the alternate set selection algorithms as well as the methods for testing the loss of a given alternate set. The _BetaLearner_ class takes in numerous instances over which to learn the betas (for later use to estimate the dropout probabilities).
* __plotter.py__: This file has helper functions for making plots.
* __pkl_jar.ipynb__: The simulations in main.py dump their output to pkl files (they can also plot their output immediately if the plotting lines are uncommented). This notebook then reads in the pkl files and produces all of the plots for the paper.

Please contact Carmel Baharav (cbaharav@ethz.ch) with any questions or comments.