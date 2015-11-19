# NurseBioCrawler
#! All python code are based on Python 3.5
Scarp nurse twitter information and extract features for further analysis. 

Quick start:
Use crawler.py to scrape nurse twitter user from followerwonk.com. This step will generate a json file for you. Since the whole procee takes a long time to finishi. I uploaded an example json file(profile100-200v3.json) for testing.
Next step you wanna use json2csv.py to convert json file to csv file. I also provided an example annoateted csv file("totalProfile.txt") for testing. You may wanna shuffle the csv file a little bit using csvShuffler.py.

After that you can use wordanalysis.py to analysis the data and generate some necessary files for feature extraction.
Then run feature_extrator.py to extract features from data. The generated file features.csv is for further classification by WEKA.


