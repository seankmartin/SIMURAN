# SIMURAN
Simultaneous Multi-Region Analysis.
The general design is to have single objects with large amounts of information and an intuitive system to set this up.

# Installation
```
git clone https://github.com/seankmartin/PythonUtils
cd PythonUtils
pip install -e .
cd ..
git clone https://github.com/seankmartin/SIMURAN
cd SIMURAN
pip install -e .
```

## Requirements
Describe what is in your data and facilitate batch processing.
Provide some analysis methods and allow for easy creation of further analyses.

## Ideas
Interface with other programs such as SpikeInterface to allow for many different systems and sorters to be used.

## Information in an experiment
1. Date and time
2. Channel map (like spike sorters)
3. Parameters file

## Information in a signal
1. Date and time (or just time).
2. Region
3. Geometrical Location
4. Tag
5. Source data location
6. File format
7. Description
8. Sampling rate
9. Duration
10. Data type

## TODO
1. Add build system.
2. Add more unit test cases
3. Make unit test cases with small data and store that data.

## Inspiration
1. https://github.com/seankmartin/NeuroChaT
2. https://github.com/SpikeInterface
3. https://github.com/seankmartin/NeuroChaT_API_Scripts
