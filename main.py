import subprocess
import os
import shutil
from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Example usage:
# delete_directory('/path/to/your/directory')
def delete_directory(directory):
    shutil.rmtree(directory)


# Example usage:
# files = get_files_in_directory('/path/to/your/directory')
# for file in files:
#     print(file)

def get_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


# Example usage
# module_name = 'my_module'
# arguments = ['--arg1', 'value1', '--arg2', 'value2']
# call_module(module_name, arguments)

def call_module(module_name, arguments):
    command = ['python', '-m', module_name] + arguments
    subprocess.call(command)

# Create zip of a directory
# Example usage:
# zip_directory('/path/to/your/directory', '/path/to/your/directory.zip')
def zip_directory(directory, zip_file):
    shutil.make_archive(zip_file, 'zip', directory)


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

def clean_up():
    if os.path.exists('output_mmCIF'):
        shutil.rmtree('output_mmCIF')
    if os.path.exists('output_PDB'):
        shutil.rmtree('output_PDB')
    if os.path.exists('PDB'):
        shutil.rmtree('PDB')
    if os.path.exists('SIFTS'):
        shutil.rmtree('SIFTS')
    if os.path.exists('mmCIF'):
        shutil.rmtree('mmCIF')
    if os.path.exists('log_corrected.txt'):
        os.remove('log_corrected.txt')
    if os.path.exists('log_translator.txt'):
        os.remove('log_translator.txt')
    if os.path.exists('output_mmCIF.zip'):
        os.remove('output_mmCIF.zip')

@app.get("/pdbrenum", response_class=FileResponse)
async def read_item(rfla: str, mmCIF: str = 'false', PDB: str = 'false'):
    clean_up() 
    module_name = 'PDBrenum'
    out_dir = 'output_mmCIF' if mmCIF == 'true' else 'output_PDB'
    arguments = []
   
    if mmCIF == 'true':
        arguments.append('-mmCIF')
    elif PDB == 'true':
        arguments.append('-PDB')

    ids = rfla.split(' ')
    for id in ids:
        call_module(module_name, ['-rfla', id] + arguments)
    # call_module(module_name, arguments)

    zip_directory(out_dir, out_dir)

    # result = FileResponse(f"{out_dir}.zip", media_type="application/zip", filename=f"{rfla[0:4]}.zip")
    return f"{out_dir}.zip"

    

    

