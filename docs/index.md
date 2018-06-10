matSHEEP
========

This library is a programmatic interface in python to generate a circuit
for the bigger and more useful SHEEP library.

The library has a few data types :

-   variables - A single bit (Could also be used as a normal scalar)
-   enc\_vec - One dimensional bit vector (Could be used a one
    dimensional vector of any data type)
-   enc\_mat - Two dimensional bit matrix (Could be used a one
    dimensional vector of any data type)
-   enc\_tensor3 - Three dimensional bit tensor.

To create a circuit, the basic class to inherit is `mini_mod` in
`mathsheep.interactions`. To add more components, you can use
`self.add(component)` inside the `create` function as shown below.:

    class oneb_adder(mini_mod):
         def __init__(self, name, inputs, outputs, nb=None,
                         randomize_temps=1, carry=True):
          mini_mod.__init__(self, name, inputs, outputs)
              self.create(...)

         def create(self, ...):
               self.add(..)

Two types of components can be added.

-   Assignments (`from matSHEEP.interactions`)

    > -   mono\_assign
    >     -   alias
    >     -   negate
    > -   bi\_assign
    >     -   xor
    >     -   and
    >     -   or
    >     -   constand
    > -   tri\_assign
    >     -   mux

-   Other mini\_mods

There are a few predefined mini\_mods. They can be found in

-   

    `matSHEEP.reusable_modules`

    :   -   oneb\_adder - Add two bits
        -   nb\_adder - Adders x and y with incoming carrt where input
            is `[cin x y]`
        -   nb\_adder\_xy - Adds x and y with `input = (x, y)`
        -   compare\_cp - Compares ciphertext with plaintext with
            `input = (c,p)`

-   

    `matSHEEP.functions`

    :   -   reduce\_add - Counts the number of ones in a bit vector.

-   

    `matSHEEP.nn_layer`

    :   -   sign\_fn
        -   linear\_layer\_1d - Inner Product of a weight vector with
            encrypted bit vector followed by a sign function.
        -   linear\_layer - Inner Product of a weight matrix with an
            encrypted bit vector followed by a sign function.
        -   conv\_layer - A convolution Layer. (Look at examples)

-   

    `matSHEEP.vector_ops`

    :   -   vec\_mono\_op\_cond - Takes a plaintext `cond` vector, a
            plaintext tuple `ass_types` containing only `alias` and
            `negate` as values and an encrypted bit vector `input`. It
            outputs an encrypted bit vector where the ith position has
            the `ass_types[cond[idx]]` operation applied on
            `input[idx]`.
        -   Similar operation for matrix and tensor.

You can also visualize the circuits you create. `test.sheep` is a circuit file.::

:   import sys import matSHEEP.create\_graph as cg complete\_node =
    cg.get\_circuit\_graph(\'./test.sheep\') ng =
    cg.networkx\_graph(complete\_node) ng.draw()

And you can get .. image:: images/LL4.png For more high level operations
and results using layers of Neural Networks visit this markdown
