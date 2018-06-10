========
matSHEEP
========

This library is a programmatic interface in python to generate a circuit for the bigger and more useful SHEEP library.

The library has a few data types :

* variables - A single bit (Could also be used as a normal scalar)
  
* enc_vec - One dimensional bit vector (Could be used a one dimensional vector of any data type)

* enc_mat - Two dimensional bit matrix (Could be used a one dimensional vector of any data type)

* enc_tensor3 - Three dimensional bit tensor.


To create a circuit, the basic class to inherit is ``mini_mod`` in ``mathsheep.interactions``. To add more components, you can use ``self.add(component)`` inside the ``create`` function as shown below.::

  class oneb_adder(mini_mod):
       def __init__(self, name, inputs, outputs, nb=None,
                       randomize_temps=1, carry=True):
	    mini_mod.__init__(self, name, inputs, outputs)
            self.create(...)

       def create(self, ...):
    	     self.add(..)

   
Two types of components can be added.

* Assignments (``from matSHEEP.interactions``)

   - mono_assign

     + alias
     + negate
   
   - bi_assign
   
     + xor
     + and
     + or
     + constand
   
   - tri_assign
     
     + mux

* Other mini_mods
   
There are a few predefined mini_mods. They can be found in

* ``matSHEEP.reusable_modules``
   - oneb_adder - Add two bits
   - nb_adder  - Adders x and y with incoming carrt where input is ``[cin x y]``
   - nb_adder_xy - Adds x and y with  ``input = (x, y)``
   - compare_cp - Compares ciphertext with plaintext with ``input = (c,p)``

* ``matSHEEP.functions``
   - reduce_add - Counts the number of ones in a bit vector.

* ``matSHEEP.nn_layer``
   - sign_fn
   - linear_layer_1d - Inner Product of a weight vector with encrypted bit vector  followed by a sign function.
   - linear_layer - Inner Product of a weight matrix with an encrypted bit vector followed by a sign function.
   - conv_layer - A convolution Layer. (Look at examples)

* ``matSHEEP.vector_ops``
   - vec_mono_op_cond - Takes a plaintext ``cond`` vector, a plaintext tuple ``ass_types`` containing only ``alias`` and ``negate`` as values and an encrypted bit vector ``input``. It outputs an encrypted bit vector where the ith position has the ``ass_types[cond[idx]]`` operation applied on  ``input[idx]``.
   - Similar operation for matrix and tensor.

You can also visualize the circuits you create. ``test.sheep`` is a circuit file.::

    import sys
    import matSHEEP.create_graph as cg
    complete_node = cg.get_circuit_graph('./test.sheep')
    ng = cg.networkx_graph(complete_node)
    ng.draw()

And you can get

.. image:: https://raw.githubusercontent.com/amartya18x/matSHEEP/master/images/LL4.png

gFor more high level operations and results using layers of Neural Networks visit this markdown
