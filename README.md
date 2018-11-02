# Scimitar
Scimitar is an visual application designed for large parameter-space exploration of numerical simulations in the physical sciences. This software is designed to work with custom numerical simulation applications which accepts a given set of parameters as input to produce some result. Scimitar automates the process of configuring, organizing, executing, and monitoring a large number of runs on single machine or a large computing cluster which iterate over one or more parameters. In the broadest sense, Scimitar takes an "embarrassingly parallel" approach by using an allocated set of computing resources and simultaneously executing many lightly-threaded instances of a simulation at once. In practice, Scimitar's goal is to automatically generate a Python script which will easily execute an instance of a program for each combination of selected parameters in a highly organized fashion, which simplifies data reduction and post-processing.

This application is used extensively within our quantum matter theory research group to simplify and streamline our workflow. Scimitar requires an installation of [wxPython](wxpython.org) running on Python 3. Execute the script `source_py35/Scimitar.py` to begin. A help file is available within the application for more information on how to use it.

_Please note that the official repository is kept on another server, so this portfolio may not contain the latest updates._
