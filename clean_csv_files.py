import pandas as pd

# directories
org = "../aclImdb/"
testPath = org + "test/"
trainPath = org + "train/"

# files concerned
fileList = [testPath + "urls_neg.csv",
            testPath + "urls_pos.csv",
            trainPath + "urls_neg.csv",
            trainPath + "urls_pos.csv",
            trainPath + "urls_unsup.csv"]