# under normal circumstances, this script would not be necessary. the
# sample_application would have its own setup.py and be properly installed;
# however since it is not bundled in the sdist package, we need some hacks
# to make it work

#  para import relativos ver https://github.com/arruda/relative_import_example

import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(1, parent_dir)

sys.path.append(os.path.dirname(__name__))

from app import create_app

# create an app instance
app = create_app()
app.debug = True

app.run(threaded=True)
