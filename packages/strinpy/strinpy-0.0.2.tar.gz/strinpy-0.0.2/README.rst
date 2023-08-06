React like string builder
=========================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: http://opensource.org/licenses/MIT
.. image:: https://badge.fury.io/py/strinpy.svg
    :target: https://badge.fury.io/py/strinpy

Usage
-----

.. code:: python

    import strinpy

    condition = True
    output = strinpy.build([
        'text',
        condition and 'condition text',
        condition and ['condition text list'],
        condition and (lambda: 'supplier text'),
        [
            'text list',
            [
                'in text list'
            ]
        ]
    ])
    print(output)
    """
    text
    condition text     
    condition text list
    supplier text      
    text list
    in text list
    """
