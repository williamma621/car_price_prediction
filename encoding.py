import pandas as pd
def onehot(df):
    categorical_cols = ['make', 'model', 'body', 'trim', 'exteriorColor', 
                    'interiorColor', 'transmission', 'driveTrain']
    return pd.get_dummies(df, columns=categorical_cols)
def target(df):
    '''
    for i in range(len(df)):
        for j in categorical_cols:
            target_string = df.iloc[[i]][j][i]
            curr_dict = target_values[j]
            if target_string in curr_dict:
                curr_dict[target_string][0] += df.iloc[[i]]['basePrice'][i]
                curr_dict[target_string][1] += 1
            else:
                curr_dict[target_string] = [df.iloc[[i]]['basePrice'][i], 1]
    for i in target_values:
        for j, k in target_values[i].items():
            target_values[i][j] = target_values[i][j][0] / target_values[i][j][1]
    '''
    categorical_cols = ['make', 'model', 'body', 'trim', 'exteriorColor', 
                    'interiorColor', 'transmission', 'driveTrain']
    target_values = {'make': {}, 'model': {}, 'body': {}, 'trim': {}, 'exteriorColor': {}, 
                    'interiorColor': {}, 'transmission': {}, 'driveTrain': {}}
    for i in categorical_cols:
        mean_price = df.groupby(i)['basePrice'].mean().to_dict()
        df[i] = df[i].map(mean_price)
        target_values[i] = mean_price
    return df, target_values

