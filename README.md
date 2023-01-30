# OutputStabilization
OutputStabilization is a control algorithm that finds a control input combination that can stabilize specific output nodes of Boolean networks in a desired state. A related paper will be published soon.

## Installation
You can simply download OutputStabilization from this git repository, while setup.py is not provided. OutputStabilization is executed on any operating system (Windows, Mac OS, Linux, etc), but Python 3.5 or higher versions must be installed to run the program.

## Usage
Write a Boolean network form as shown below in the modeltext variable at the bottom of the code, and write the output node and the desired state as True or False in the form of a dictionary in the targetDic variable.
```
modeltext = '''
x01 = not x06 and not x04
x02 = x01 or (x07 and x05) or (x03 and x02)
x03 = x01
x04 = (x08 and x07) or (x08 and x05)
x05 = (x07 and x08 and x03) or (x08 and x03 and x01)
x06 = x06 and not x08
x07 = (x02 and x01 and x06) or (x02 and x01 and x07)
x08 = x04 and not x02 and not x01
x09 = x03
x10 = x08 or (x05 and x02) or x11
'''
targetDic = {'x09': True, 'x10': True}
```

## Output
Control input(s) that can control the set output node to the desired state are output.
```
[{'x03': True, 'x11': True}, {'x01': True, 'x11': True}, {'x01': True, 'x05': True}]
```
