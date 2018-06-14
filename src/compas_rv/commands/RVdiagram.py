#import time
#
#tic = time.time()
#
from sys_path_import import sys_path_init
sys_path_init()

from compas_rv.interface.io import initiate_mesh


if __name__ == '__main__':
    initiate_mesh('Default')
   



