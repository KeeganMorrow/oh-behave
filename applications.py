import logging
import oh_behave
from oh_behave import behave
from oh_behave import actor
from oh_behave import action
from oh_behave import reader

logger = logging.getLogger(__name__)

def main():
    json_objects = [
        '{\n' \
        '        "id": "actor_01",\n' \
        '        "type": "Actor",\n' \
        '        "name": "Billy Bob",\n' \
        '        "rootnode": "noderoot"\n' \
        '}',
        '{\n' \
        '        "id": "noderoot",\n' \
        '        "type": "NodeSequence",\n' \
        '        "name": "Root Node",\n' \
        '        "childnodes": ["node01", "node04"]\n' \
        '}',
        '{\n' \
        '        "id": "node01",\n' \
        '        "type": "NodeSelector",\n' \
        '        "name": "Fix Computer",\n' \
        '        "childnodes": ["node02_n", "node03"]\n' \
        '}',
        '{\n' \
        '        "id": "node02_n",\n' \
        '        "type": "NodeDecoratorInvert",\n' \
        '        "name": "inverter",\n' \
        '        "decoratee": "node02"\n' \
        '}',
        '{\n' \
        '        "id": "node02",\n' \
        '        "type": "NodeSequence",\n' \
        '        "name": "Smack it"\n' \
        '}',
        '{\n' \
        '        "id": "node03",\n' \
        '        "type": "NodeSequence",\n' \
        '        "name": "Smack it harder"\n' \
        '}',
        '{\n' \
        '        "id": "node04",\n' \
        '        "type": "NodeSequence",\n' \
        '        "name": "Relax"\n' \
        '}'
        ]
    logger.info('Entering main')

    parser = reader.DataParser()
    for string in json_objects:
        parser._parse_object_string(string)
    objects = parser.build_objects()
    status = oh_behave.ExecuteResult.ready
    while status is oh_behave.ExecuteResult.ready:
        status = objects['actor_01'].execute()

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    main()
