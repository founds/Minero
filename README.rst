Minero
-----------

**Raptor** for extracting and displaying information from a set of files of the same type; and creating a single CSV file with all the selected information.

The information in the files may be in multiple rows::

    GMM().get_urls(
    keys=['Fresas', 'Tomates', 'Cebollas', 'Ajos'],
    prefixs=['Plantar', 'Sembrar'],
    subfixs=['Maceta', 'Jardineras'])

    GMM().process_urls(
    keys=['Fresas', 'Tomates', 'Cebollas', 'Ajos'])

