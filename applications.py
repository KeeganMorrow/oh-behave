import logging
import oh_behave
from oh_behave import behave
from oh_behave import actor
from oh_behave import action
from oh_behave import reader

logger = logging.getLogger(__name__)

def main():
    input_string1 = '{\n' \
        '        "id": "actor_01",\n' \
        '        "type": "Actor",\n' \
        '        "name": "Billy Bob",\n' \
        '        "rootnode": "noderoot"\n' \
        '}'
    input_string2 = '{\n' \
        '        "id": "noderoot",\n' \
        '        "type": "NodeSequence",\n' \
        '        "name": "Root Node"\n' \
        '}'

    logger.info('Entering main')

    parser = reader.DataParser()

    parser._parse_object_string(input_string1)
    parser._parse_object_string(input_string2)
    objects = parser.build_objects()

    objects['actor_01'].execute()
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    main()
