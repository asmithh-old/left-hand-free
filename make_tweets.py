import os, ast
with open(os.path.expanduser('~/Desktop/model.csv')) as f:
    content = f.readlines()
    wts = ast.literal_eval(str(content[0]))
    model = ast.literal_eval(str(content[1]))
    f.close()
