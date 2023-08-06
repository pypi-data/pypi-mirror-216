=====================
RER: Immersive reader
=====================

Immersive reader support for Plone contents.

Configuration
=============

You need to set some env variables in buildout, to get the right token:

- IMR_CLIEND_ID (client id)
- IMR_CLIEND_SECRET (client secret)
- IMR_TENANT_ID (tenant id)
- IMR_SUBDOMAIN (subdomain)

Control panel
-------------

In the control panel (*@immersive-reader-settings*) you can:

- Set a list of portal_types where the immersive reader will be enabled.

Installation
============

Install rer.immersivereader by adding it to your buildout::

    [buildout]

    ...

    eggs =
        rer.immersivereader


and then running ``bin/buildout``


Contribute
==========

- Issue Tracker: https://github.com/collective/rer.immersivereader/issues
- Source Code: https://github.com/collective/rer.immersivereader
- Documentation: https://docs.plone.org/foo/bar


Support
=======

If you are having issues, please let us know.
We have a mailing list located at: project@example.com


License
=======

The project is licensed under the GPLv2.

Compatibility
=============

This product has been tested on Plone 5.1 and 5.2


Credits
=======

Developed with the support of `Regione Emilia Romagna`__;

Regione Emilia Romagna supports the `PloneGov initiative`__.

__ http://www.regione.emilia-romagna.it/
__ http://www.plonegov.it/

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/
