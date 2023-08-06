.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.gridlisting/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.gridlisting/actions/workflows/plone-package.yml


collective.gridlisting
======================

Adds a Behavior to manipulate various listing appearance settings
using Bootstrap 5 (column layout) and patternslib (masonry).

This behavior is automatically enabled for "Folder" and "Collection" when you install it.


Features
--------

- Adds new view template "Grid listing" for "Folder" and "Collection"
- You get a new "Grid listing" tab when editing a Folder or a Collection where
  you can set various options for the listing template.


Get started
-----------

1. Install `collective.gridlisting` in the Add-ons controlpanel
2. Go to a folder and select **Grid listing** from the **Display** menu
3. Edit the folder and go to the **Grid listing** tab
4. You can enter CSS classes for the grid items and/or enable **Masonry layout**.


Grid setup
----------

The grid structure is set up as follows:

+--------------------------------+
|  Container row                 |
|                                |
|  +--------------------------+  |
|  |  Column                  |  |
|  |                          |  |
|  |  +--------------------+  |  |
|  |  |  Column content    |  |  |
|  |  |                    |  |  |
|  |  |  +------+-------+  |  |  |
|  |  |  | text | image |  |  |  |
|  |  |  +------+-------+  |  |  |
|  |  +--------------------+  |  |
|  +--------------------------+  |
+--------------------------------+

You can define css classes for each of those containers.

For example if you simply want a responsive 4/2/1 column layout you can set the ``Container row CSS class`` to:

  ``row-cols-1 row-cols-lg-2 row-cols-xl-4``

You can also define borders, margins and paddings for the column content with ``Column content CSS Class``:

  ``border border-primary m-2 p-2``

And you can further experiment with gutters or backgrounds.

Inside the column, the text and image information can be defined separately.
You can for example simply switch the order of text/image with:

  ``Column content text: col order-2``

  ``Column content image: col order-1``

or put the image above the text with:

  ``Column content text: col-12 order-2``

  ``Column content image: col-12 order-1``

For more information on the CSS definitions see the Bootstrap documentation:

https://getbootstrap.com/docs/5.3/layout/grid/


Special Example: Card listing
-----------------------------

The following values gives you a listing with cards, cell height 100% and image at the top:

- ``Container row``: ``row-cols-3`` (3 columns)
- ``Column``: ``pb-3`` (spacing below card)
- ``Column content``: ``card h-100`` (card outline, 100% cell height)
- ``Column content text``: ``order-2 card-body`` (text below image)
- ``Column content image``: ``order-1 card-img-top`` (image above text)

et voila!

NOTE: If you enable **Masonry layout** you have to remove ``h-100`` from ``Column content``
and you have a masonry card listing like shown here: https://getbootstrap.com/docs/5.3/examples/masonry/


Translations
------------

This product has been translated into

- English
- German


Installation
------------

Install collective.gridlisting by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.gridlisting


and then running ``bin/buildout``


Compatibility
-------------

Plone 6, Python 3.8 - 3.11


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.gridlisting/issues
- Source Code: https://github.com/collective/collective.gridlisting
- Documentation: https://github.com/collective/collective.gridlisting/docs



License
-------

The project is licensed under the GPLv2.
