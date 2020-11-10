import pandas as pd

# Return Max and Min X,Y Coordinate Value of file
def coorMaxMin(file: pd.DataFrame) -> (float, float, float, float):
    minX, minY = (file.loc[0][0], file.loc[0][1])
    maxX, maxY = (file.loc[0][0], file.loc[0][1])
    for i in range(0,file.shape[0]):
        x = file.loc[i][0]
        y = file.loc[i][1]
        if x > maxX :
            maxX = x
        if x < minX :
            minX = x
        if y > maxY :
            maxY = y
        if y < minY :
            minY = y
    return minX, minY, maxX, maxY