# Qwerty POOL

POOL stands for Python Operating Other Languages.
Qwerty POOL is made to operate other languages such as java and implement different opportunities such as creating windows.

## Installation

You can install Qwerty POOL from [PyPI](https://pypi.org/project/qwertyPOOL/):

    pip install qwertyPOOL

Or you can install Qwerty POOL from [Github](https://github.com/pi-this/POOL):

    git clone https://github.com/pi-this/POOL.git

## How to use

If Java is not installed already use the following command to install it:

    import qwertyPOOL
    qwertyPOOL.java.jdk()
    qwerty.java.jre()

Although Qwerty POOL's possibilities are short within version 1.0.0, it has the capability to display a window with text from java

To open a window in Qwerty POOL:

    import qwertyPOOL
    qwertyPOOL.run.do()

To Change the POOL icon:

    from qwertyPOOL import java as Lj
    Lj.window.SetImage("face.png")
    Lj.window.open()
    Lj.runj()

To Add Text to the window:

    from qwertyPOOL import java as Lj
    Lj.window.SetText("hello qwertyPOOL!")
    Lj.window.open()
    Lj.runj()
    
To View Qwerty POOL's version:
    
    qwertyPOOL.operating.version()
    
Or:

    print(qwertyPOOL.__version__)
    
To Wait in Qwerty POOL:
    
    qwertyPOOL.python.wait(2) # seconds
