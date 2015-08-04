Changelog
=========

0.2 (2015-08-04)
----------------

- Load the CMFCore zcml so we can use the permissions.  This avoids a
  possible startup error on Plone 4.
  [maurits]

- Added ``z3c.autoinclude``-entrypoint to mark this as a Plone-plugin.
  This avoids the need to explicitly load the zcml-slug.
  [WouterVH]

- Move the repository to the Plone Collective repository. [markvl]


0.1.1 (2010-02-25)
------------------

- Cleanup package. [markvl]


0.1 (2010-02-25)
----------------

- Initial release. [markvl]
