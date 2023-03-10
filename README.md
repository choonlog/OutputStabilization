# OutputStabilization
OutputStabilization is a control algorithm deriving a control input combination that can stabilize specific output nodes of Boolean networks in a desired state. A relevant paper is submitted to IEEE Trans. Neural Netw. Learn. Syst.

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
Control input(s) that can stabilize the prescribed output node(s) to their desired state are produced as the output of this code.
```
[{'x03': True, 'x11': True}, {'x01': True, 'x11': True}, {'x01': True, 'x05': True}]
```

# BNGenerator
BNGenerator is executed independently of OutputStabilization, and is a software that generates a random Boolean network using Biological Boolean logics extracted from 78 Biological Boolean networks in the Cell Collective (https://cellcollective.org/).

## Example
It can be executed by entering the parameters of the main function in line 64 of random_Boolean_network_generator_output_node.py.
```
Boolean_network = main(20, 1, 3, 2) # The parameters of main function mean the number of nodes to be included in the network, the minimum in-degree, the maximum in-degree, and the number of output nodes, respectively.
print(Boolean_network)
```
