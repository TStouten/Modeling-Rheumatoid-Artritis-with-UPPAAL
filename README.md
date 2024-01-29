# Installing the tool 

To use this tool, UPPAAL and Python must be installed on the device. The tool and models should be placed in bin-Windows directory within the UPPAAL installation folder. Once this is done, the tool can be started by running the Rheumatoid Arthritis Modeling Tool (RaMoTo) via launching the python script or via the command line by calling RaMoTo.py by the Python interpreter. 

## Loading the tool 

When the tool is started, a query appears on the command line that requests the names of the patient model, the protocol model, and the query file. These models and the query file should be in the same folder as the tool, then the full file name should be given. 

## Commands 

This tool has 9 different options that can be evoked in the main menu, with the use of the numbers 0 to 8. 

### 0 Run queries 

This command is used to send the models and queries to Verifyta. The result of each query is shown on the command line as data which can be interpreted by the user or that can be copied for further analysis. 

### 1 show protocol 

This command shows all the steps present in the protocol. 

The first line shows the initial step, followed by all query steps showing the step number, the number of weeks this step should be followed, the number of the medication being used, and the next protocol steps dependent on the disease severity of the patient. 

### 2 edit protocol steps 

This command shows all protocol steps and requests which protocol step should be edited. Once the step has been chosen, the tool will display the current settings. This value can be changed by inserting a new integer, or this setting could remain the same by not entering anything. 
Once all settings for a step have been registered, the full set is shown with a confirmation, “y” for yes and “n” for no, after which the change is saved or discarded. 

### 3 Delete protocol step 

This command shows all protocol steps and requests which protocol step should be deleted. Once the step has been chosen, a confirmation is requested where the user can write “y” to accept, "n” to decline. 

### 4 Add protocol step 

After the confirmation, “y” is given, the tool requests a step number. If this step number is not yet in use, the duration, medication and next steps are requested. After a last confirmation, this step is added to your protocol model. 

### 5 Show medicine combinations 

This command shows all medicine combinations available in the models. 
To see the transitional setting for a medicine combination, insert the name. 

### 6 Edit existing medicine combinations 

Insert the name of the medicine combination of which some settings must be changed. 
The tool first requests if the name should be changed. If “y” is inserted, you can insert a new name that is not yet in use.  After this, all current settings are shown. After each setting, enter the new value, or press enter to keep the current value. 
The tool requests confirmation after showing the new name and setting, after which the changes are saved or discarded. 

### 7 Add new medicine combination 

This command enables the user to add new medication types. The tool first requests a name that is not yet in use. If a name that is already in use is chosen, the tool will request a new name.  Once the name is given, the cost and all transition weights are requested and saved as a new type of medicine combination. 

### 8 Queries 

This command shows all available queries. Currently, there are 4 queries available. The number of runs of each query can be edited by inserting the query number, followed by the new number of runs. The higher the number of simulations used to evaluate a query increases the credibility of the result, while increasing the evaluation's duration. 

 
