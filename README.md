# ML-Engineer-Udacity

## _Predicting heart rate dynamics and internal training stress from cycling data_

### Requirements

#### Data

There are three different types of data used in this project. All three are .csv file exports from Golden Cheetah, an open source cycling software tool (https://www.goldencheetah.org/).

Examples of the three datafiles are in the **data_examples** folder. 

#### Code

In order to run this project, you will need to run the Jupyter Notebooks in the proper order. The notebooks can be found in the folder **notebooks**. The notebook are:

- 0. Data exploration.ipynb
- 1. Data processing.ipynb
- 2. Feature engineering.ipynb
- 3. Feature exploration and selection.ipynb
- 4. Modelling.ipynb
- 5. Training stress calculations.ipynb

Also the project makes use of processing and plotting functions which can be found in the folder **python_code_files**

#### Configuration

Since this project / model is specific for an individual (meaning for each individual the model should be re-estimated) the model should always be re-estimated.

In addition a rider_config file with individual parameters should be adjusted (see folder **config**)

#### Computational resources

The projec is rather "memory intensive". Most of the code was run on a local machine with the following specification: Intel® Core™ i7-8850H CPU @2.60GHz 2.59 GHz with 32GB RAM, 235 GB storage

Do note that each procedure can take a few hours to run, especially in the 4. Modelling.ipynb notebook. We ran parts of that notebook on an AWS notebook instance (ml.c5.18xlarge) and even that took quite some time (e.g. 5 hours for the cross-validation). 

Since also intermediate results are saved during or at the end of the notebooks so enough storage capacity is also needed. For reference: the modelset size with around 4mln. datapoints .pkl file is 3.5GB (3 years, ~770 ride files)

### Report

Next to code also explanations are given in the notebooks at the beginning and during processing steps. In addition, there is a report.pdf available in the **report** folder with more background and literature on the domain. Als a proposal.pdf is available in that folder. We encourage the reader to read this for more context on the project.

### Abstract

Coaches and riders can benefit from predicting heart rate dynamics before a ride (training) takes place. This insight could be used for planning purposes further downstream when multiple rides are simulated and can help to estimate training stress in advance. Moreover predicted heart rate dynamics could ex-post be compared to realized heart rate dynamics which might give further insight in the rider’s physical condition. The goal of this project is to predict heart rate dynamics and training stress before a ride takes place.

### Project design and methodology

The project uses field data from a cyclist to create a model for predicting heart rate response based on variables which could be determined before a ride takes place. Linear methods and non-linear methods are used to create a final model. In addition training stress scores are calculated and compared with scores from aggregate data models.

Also suggestions are provided to experiment further and improve model performance. 

### Copyright Notice

Feel free to use, and distribute at will. Typical machine learning project steps are documented and discussed both in a report and the notebooks. We hope this stimulates readers to start analysing and experiment with their own data. 

Do you **want to apply machine learning models on (cycling) sports data or discuss some more**? [**Get in touch with the author**](https://github.com/RuudVelo).
