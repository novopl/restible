########
restible
########

.. include:: ../README.rst
    :start-after: about_project_start
    :end-before: about_project_end

.. toctree::
    :maxdepth: 2

    tutorial/index
    Code Reference <ref/restible/index>
    contrib


.. include:: ../README.rst
    :start-after: project_links_start
    :end-before: project_links_end


.. admonition:: Project Versioning

    The project follows the semantic versioning scheme: Until 1.0 the minor

        * The *patch* versions only include bug fixes and changes that do not
          modify the existing interface. You can safely update a patch version
          without worrying it will break your code.
        * The *minor* versions will contain changes to the interface. With a
          single version update your code will most likely work or might require
          small adjustments. The more minor versions you update at once the
          bigger the chance that something will brake.
        * The *major* versions are reserved for significant refactorings and
          architecture changes. This should not happen very often so the major
          version should not change much.
