import os
dirs=[
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    os.path.join("data","split")
    os.path.join("data","transformed_data"),
    "notebooks",
    "src",
    "webapp",
    "tests"
    
    
    "saved_models"
      ]

for dir_ in dirs:
    os.makedirs(dir,exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass
    
# files=[
#     "dvc.yaml",
#     "params.yaml",
#     ".gitingnore",
# ]

# for file_ in files:
#     with open(file_,"w") as write:
#         pass

for dir_ in dirs:
    os.makedirs(dir_, exist_ok=True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:
        pass
