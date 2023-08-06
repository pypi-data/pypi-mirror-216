

from collections import namedtuple


ArtefactSpec = namedtuple('ArtefactSpec',
                          'label type access required unique',
                          defaults=("Member", False, False))
