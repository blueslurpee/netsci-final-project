# MINF4573 Network Science Final Project - Herbstsemester 2021
### Corey Bothwell, Maria Helena Margareta Pelli, Pascal Liniger

We analyse the following ERC-721 token networks for their network properties in order to investigate their interplay and relationship to price movements.

- Bored Ape Yacht Club
- Coolcats
- Cryptoadz
- Cyberkongz
- Hashmasks
- Mutant Ape Yacht Club
- Meebits
- Mekaverse
- Sneaky Vampire Syndicate

![BAYC Network 2021 JUL 16](https://github.com/blueslurpee/netsci-final-project/blob/master/BAYC_20210716.png?raw=true)

The accompanying submission includes the report, slides, video, as well as the code and the supplementary materials. This repository is provided as a reference.

# Setup

The repository has the following structure:

```
--project
|-- data
|-- eda
|-- memory
|-- output
|-- .gitignore
|-- 1_ingest.ipynb
|-- 2_analysis.ipynb
|-- 3_plot.ipynb
|-- BAYC_20210716.png
|-- README.md (This file)
```

The `data` directory contains the raw data pulled from Etherscan.io and the Ethereum blockchain, as well as the accompanying scripts to generate the data.
The raw data was loosely modeled off the following work [Networks of Ethereum Non-Fungible Tokens: A graph-based analysis of the ERC-721 ecosystem](https://arxiv.org/abs/2110.12545)
We recommend most users interested in the raw data to simply use the provided csv files present at `./data/collated`.

The `eda` directory contains some additional data analysis performed by the team.

The `memory` directory stores persistent representations of the dataframes and graph objects used in the analysis. They are generated from the raw data and saved in order to allow the analysis to be quickly repeated.
The `output` directory stores images of our chart output. These directories can be mostly ignored.

# The Main Files

We recommend most readers simply re-run `2_analysis.ipynb` which provides reproducible results and runs "out of the box" assuming all python dependencies are installed. If readers want to re-generate the dataframes or graph objects, see `1_ingest.ipynb`.

### `1_ingest.ipynb`

This notebook generates analysis dataframes and graphs for the networks.

References to these projects and their respective smart contracts can be found in the accompanying report. 
The notebook first generates **general analysis** dataframes pulling from each project csv file found in the `./data/collated` directory. The notebook persists these dataframes at `./memory/<project>/full.npy` before creating the graph objects from them. 

Thus, if you want to change the graph models (as we needed to many times over the course of this project), you can do so without re-generating the dataframes themselves. If you only want to generate the graph objects and not the dataframes from scratch, set the `GENERATE_DATAFRAMES` variable in the config section in order to control this behavior.

The graphs are then generated from each dataframe as ten successive snapshots of the network. Each snapshot is inclusive of those that came before-hand. In short, the snapshots capture the evolution of the network at different times. Each snapshot is stored at `./memory/<project>/snapshots/` along with a summary dataframe. There is also a `GENERATE_GRAPHS` config variable available as well, which functions analogously to its sibling variable for the dataframes. Note that if both of these variables are set to `False`, the notebook won't produce any output.

You can also set the `TEST_LIMIT` config variable, which is helpful for debugging. This limits the anaylsis to the first X rows of the csv files. Note that that upon a successful run the dataframe object will be overwritten, so stash your changes or save a copy in order to restore. 

The notebook is written in a straightforward and functional style in the attempt to minimize any bloat and be supremely understandable for the reader. Very few of the cells actually run any processes, most are simple function declarations.

If you downloaded this project from the github repository, the necessary dataframes and graph snapshots are already generated for you. You can then run them in the `2_analysis.ipynb` notebook.

The notebook has one network dependency in the Coinbase API. Set the environment variables in order to re-run the notebook successfully. This API is used for the ETH-USD conversion rate. Although we generated persistent representations of this data, we used this API for filling in any gaps. Note this is not required if all you want to do is generate the graphs. In that case, simply comment out this portion and set `GENERATE_DATAFRAMES` to `False`.

### `2_analysis.ipynb`

This notebook pulls the pre-generated dataframes and network objects which have been generated by `1_ingest.ipynb` from the filesystem and the produces some useful analysis.
As the data generation is split from the analysis code, this notebook can be run relatively quickly. Like the first notebook, the notebook is written in a very functional style in order to allow for readability. Plotting functions are declared and then called to minimized bloat.

### `3_plot.ipynb`

This notebook contains the code for generating the visualisation of the BAYC network. It could be feasibly adopted to any of the other networks.
