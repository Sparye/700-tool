import shutil
import os
import astor
from tree_util import has_node,has_validation_split,load_tree,add_validation_split
from modify_tree import modify_tree,add_imports

if __name__ == '__main__':
    print("==============================")
    print("INPUT")
    print("==============================")
    # while True:
    #     filename = input("Please specify the directory location of the project code:")
    #     # Check directory exists
    #     if os.path.isdir(filename):
    #         break
    #     print("Oops, sorry that file does not exist or isn't a directory! Try again...")
    filename = "df-testing"
    # print(filename)
    if os.path.exists(filename + "_modified"):
        shutil.rmtree(filename + "_modified")
    shutil.copytree(filename, filename + "_modified")
    filename = filename+"_modified"
    for dir in os.listdir(filename):
        parentDir = filename+os.sep+dir
        for pythonFile in os.listdir(parentDir):
            if pythonFile.endswith(".py"):
                targetFile = parentDir+os.sep+pythonFile
                tree = load_tree(targetFile)
                if has_node("fit",tree) and has_node("evaluate",tree) and has_node("compile",tree):
                    print("processing file: "+targetFile)
                    if not has_validation_split(tree):
                        tree = add_validation_split(tree)
                # if has_validation_split(tree):
                    tree = add_imports(tree)
                    with open(targetFile,'w') as myfile:
                        myfile.write(astor.to_source(tree))
                    tree = load_tree(targetFile)
                    tree = modify_tree(tree,dir,pythonFile)
                    with open(targetFile,'w') as myfile:
                        myfile.write(astor.to_source(tree))
                    print("Successfully processed: "+targetFile)
                    # else:
                    # print("Failed to process: " + targetFile)
                    print("==================================")

