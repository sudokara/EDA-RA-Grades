import pandas as pd

raw_df = pd.read_excel("./Real Analysis Master Copy.xlsx")

# Convert from object datatype to float where needed and drop the erronous rows where conversion is not possible
convert_to_float = ['Quiz2', 'Assignment 2', 'End Exam']
for column in convert_to_float:
    raw_df[column] = pd.to_numeric(raw_df[column], errors='coerce')    
raw_df = raw_df.dropna(subset=['Assignment 2', 'Quiz2', 'End Exam'])


# Remove identifying columns
raw_df.drop(['Username', 'First name', 'Surname'], axis='columns', inplace=True)


# Keeping only course code from ID number
raw_df['ID number'] = raw_df['ID number'].apply(lambda x: str(x)[4:7])


# Adding branch column
codes_to_branch = {
    '101': 'CSE',
    '102': 'ECE',
    '111': 'CSD',
    '112': 'ECD',
    '113': 'CND',
    '160': 'IDK'
}
raw_df['Branch'] = raw_df['ID number'].apply(lambda x : codes_to_branch[x])


# Dropping ID number column since it is no longer needed
raw_df.drop('ID number', axis='columns', inplace=True)


# Adding 'Is Dual Degree' column
dual_branches = ['CSD', 'ECD', 'CND']
raw_df['Is Dual Degree'] = raw_df['Branch'].apply(lambda x : x in dual_branches)


# Separate data frame for those whose grades are not confirmed yet (grade has a prefix of 'X')
unfinished_df  = raw_df[raw_df['Grade'].apply(lambda x : str(x)[0] == 'X')]


# Separate dataframe for those whose grades are confirmed
finished_df = pd.concat([unfinished_df, raw_df]).drop_duplicates(keep=False)


# writing to csv
raw_df.to_csv("raw.csv")
finished_df.to_csv("finished.csv")
unfinished_df.to_csv("unfinished.csv")

