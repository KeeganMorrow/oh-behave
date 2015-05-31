import oh_behave
from oh_behave import behave
from oh_behave import actor
from oh_behave import action

def main():

    root = behave.NodeSelector('selector')
    billybob = actor.Actor("Billy bob", root)

    it1 = behave.NodeLeafAction('leaf1', action.ActionTimed(billybob, 2))
    it2 = behave.NodeDecoratorInvert('inv', behave.NodeLeafAction('leaf2', action.ActionTimed(billybob, 1)))
    it3 = behave.NodeLeafAction('leaf3', action.ActionTimed(billybob, 3))
    it4 = behave.NodeLeafAction('leaf4', action.ActionTimed(billybob, 1))

    seq1 = behave.NodeSequence('sequence1')
    seq1.addchild(it1)
    seq1.addchild(it2)

    seq2 = behave.NodeSequence('sequence2')
    seq2.addchild(it3)
    seq2.addchild(it4)

    root.addchild(seq1)
    root.addchild(seq2)


    status = oh_behave.ExecuteResult.ready
    while status == oh_behave.ExecuteResult.ready:
        status = billybob.execute()

main()
