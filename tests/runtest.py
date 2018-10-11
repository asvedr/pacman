from logic.field import Field

import os

sample = 'sample.txt'

field = Field(os.path.join(os.path.dirname(__file__), sample))

print(field)
