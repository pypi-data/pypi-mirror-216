

""""""# start delvewheel patch
def _delvewheel_init_patch_1_3_8():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'benanalysis.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_init_patch_1_3_8()
del _delvewheel_init_patch_1_3_8
# end delvewheel patch

#
# @file __init__.py
# @author Markus Führer
# @date 5 May 2023
# @copyright Copyright © 2023 Bentham Instruments Ltd. All Rights Reserved.
#

#
# @file __init__.py
# @author Markus Führer
# @date 5 May 2023
# @copyright Copyright © 2023 Bentham Instruments Ltd. All Rights Reserved.
#

from benanalysis._benpy_core import *