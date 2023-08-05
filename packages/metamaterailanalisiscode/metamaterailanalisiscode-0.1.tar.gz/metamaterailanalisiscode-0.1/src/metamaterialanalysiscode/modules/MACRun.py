"""
Module for running the .fem files in optistruct
"""
from subprocess import run
import os
from time import sleep
from shutil import move

def run_optistruct(path: str, numcores: int) -> None:
    """
    Function that runs the .fem file using optistruct. It should be the same as given for MACAnalysis.write()
    The number of cores is given by the user. Don't surpass the number of cores of your computer.
    """
    # Code that runs the .fem file using optistruct
    run([r"C:\Program Files\Altair\2022\hwsolvers\scripts\optistruct.bat", path, "-nt", str(numcores)])


def secuencial_run_optistruct(directory: str, numcores: int) -> None:
    """
    Function that runs the .fem files in a directory using optistruct.
    The number of cores is given by the user. Don't surpass the number of cores of your computer.
    """

    fem_files = {file for file in os.listdir(directory) if file.endswith(".fem")}
    for fem_file in fem_files:

        # Creo una nueva carpeta con el nombre del archivo .fem
        newdirectory = os.path.join(directory, fem_file.split(".")[0])
        os.makedirs(newdirectory)

        # Muevo el archivo .fem a la nueva carpeta
        move(os.path.join(directory, fem_file), newdirectory)

        # Ejecuto el archivo .fem
        run_optistruct(os.path.join(newdirectory, fem_file), numcores)

        # Espero a que se cree el archivo .h3d
        while not fem_file.split(".")[0] + ".h3d" in os.listdir(directory):
            sleep(5)
            for runing_file in os.listdir(directory):
                if not runing_file.endswith(".txt") and not runing_file.endswith(".message"):
                    break
        # Una vez creado, paso al siguiente archivo


# path where this code is executed
path = os.path.dirname(os.path.abspath(__file__))

secuencial_run_optistruct(path, 20)

