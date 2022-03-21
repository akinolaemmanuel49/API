#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='repository',
         url='postgresql://bit:password@0.0.0.0/db', debug='False')
