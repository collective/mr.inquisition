*Nobody expects the Plone inquisition!*

Introduction
============

This package helps with getting insight in a foreign Data.fs.

Some Plone projects can start from scratch: the customer wants to make
a (new) start with Plone and there is no legacy to take into
account. Other projects start with a Plone site already in place.

In these situations it is often a big surprise what you are going to
have to deal with. Especially when migrating a site from one Plone
version to another. Typical questions are:

* What type of objects can I expect?

* What is the number of objects for type X?

* Where does most of the content live?

* Are there objects left of products that were once installed?

Mr.inquisition helps to get answers to these questions. This package has been
tested on Plone versions 2.5 and 3.x.


Installation
============

When you are using zc.buildout, the installation is quite simple. All you
need to do is make sure the ``mr.inquisition`` package is listed in the
``eggs`` and ``zcml`` sections, e.g.::

  [buildout]
  ...
  eggs =
      ...
      mr.inquisition

  [instance]
  ...
  zcml =
      mr.inquisition

That's it.

If you want to use mr.inquisition on a site that doesn't use buildout or eggs,
you can also copy the ``inquisition`` folder from the mr.inquisition egg to the
``Products`` directory op your instance.


Usage
=====

The mr.inquisition package offers a number of views which allow you to
gain insight in the ZODB at hand. Your best bet is to start with the
``@@inquisition`` view. This view lists all the options you've got.
