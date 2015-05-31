from mod import behave
from mod import actor

def main():
    it1 = behave.NodeLeafIterative('leaf1', 4)
    it2 = behave.NodeLeafIterative('leaf2', 7)

    child = behave.NodeSequence('sequence')

    child.addchild(it1)
    child.addchild(it2)


    root = behave.NodeSelector('selector')
    root.addchild(child)

    billybob = actor.Actor("Billy bob", root)

    status = behave.ExecuteResult.ready
    while status == behave.ExecuteResult.ready:
        status = billybob.execute()

main()
