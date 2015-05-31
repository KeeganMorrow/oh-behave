from mod import behave
from mod import actor

def main():
    it1 = behave.NodeLeafIterative('leaf1', 2)
    it2 = behave.NodeDecoratorInvert('inv', behave.NodeLeafIterative('leaf2', 1))
    it3 = behave.NodeLeafIterative('leaf3', 3)
    it4 = behave.NodeLeafIterative('leaf4', 1)

    seq1 = behave.NodeSequence('sequence1')
    seq1.addchild(it1)
    seq1.addchild(it2)

    seq2 = behave.NodeSequence('sequence2')
    seq2.addchild(it3)
    seq2.addchild(it4)

    root = behave.NodeSelector('selector')
    root.addchild(seq1)
    root.addchild(seq2)

    billybob = actor.Actor("Billy bob", root)

    status = behave.ExecuteResult.ready
    while status == behave.ExecuteResult.ready:
        status = billybob.execute()

main()
