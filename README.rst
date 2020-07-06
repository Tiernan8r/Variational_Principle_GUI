=================================
**The Variational Principle GUI**
=================================
---------------------------------------------------------
A graphical user interface for the Variational Principle:
---------------------------------------------------------

*https://github.com/Tiernan8r/Variational-Principle*

-----------------------------------------------------

Usage:
=============

Before starting with anythin else, make sure python 3 is downloaded and installed on your computer. 

Download the code to your computer either by downloading the zip from Code/Zip above, or by running::
git clone https://github.com/Tiernan8r/Variational-Principle-GUI

If you downloaded the zip, unzip the directory, and go to that directory, otherwise just go to the location where the repository was cloned.

Using the terminal, or command prompt on Windows, run::
pip install -r requirements.txt

The programme can now be run by running ``main.py`` through your file explorer or while still on the command line running::
python main.py

Installation:
=============

The program can be installed to an executable from the command line:
*Note: you will most likely need to run these commands as superuser or administrator*
While still in the command line and in the top level directory run::
pyinstaller -F ./main.py -n variational_principle_gui --hidden-import=pkg_resource.py2_warn
