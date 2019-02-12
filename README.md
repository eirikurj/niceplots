# README #

### What is this repository for? ###

* A collection of small tweaks to improve Python / plotting

### How do I install? ###

* Clone this repository, then enter the folder in the command line terminal.
* Enter `pip install -e .` within the `niceplots` folder.

### How do I get set up? ###

* Use 'import niceplots' at the top of a file where you would like to use any function defined in this package.
* Use 'niceplots.all()' after all the plot commands to apply the niceplot standards on the figure
* To use the Matlab colormap "parula", execute `from niceplots import parula` then use `parula.parula_map` as your colormap within your plotting script. For example, ` plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto', cmap=parula.parula_map)`

### Contribution guidelines ###

* Make any changes you see fit. Please fork your own version and submit a pull request.

### Who do I talk to? ###

* Any MDO Lab member
* John Jasa, johnjasa@umich.edu
