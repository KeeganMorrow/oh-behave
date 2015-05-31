import oh_behave
from oh_behave import behave
from oh_behave import actor
from oh_behave import action

def main():

    root = behave.NodeSelector(name='selector')
    billybob = actor.Actor(name="Billy Bob", rootnode=root)

    it1 = behave.NodeLeafAction(name='leaf1', action=action.ActionTimed(actor=billybob, name='sleep', timegoal=2))
    it2 = behave.NodeDecoratorInvert(name='inv', decoratee=behave.NodeLeafAction(name='leaf2', action=action.ActionTimed(actor=billybob, name='mine gold', timegoal=1)))
    it3 = behave.NodeLeafAction(name='leaf3', action=action.ActionTimed(actor=billybob, name='cause trouble', timegoal=3))
    it4 = behave.NodeLeafAction(name='leaf4', action=action.ActionTimed(actor=billybob, name='look at cat pictures', timegoal=1))

    seq1 = behave.NodeSequence(name='sequence1')
    seq1.addchild(it1)
    seq1.addchild(it2)

    seq2 = behave.NodeSequence(name='sequence2')
    seq2.addchild(it3)
    seq2.addchild(it4)

    root.addchild(seq1)
    root.addchild(seq2)


    status = oh_behave.ExecuteResult.ready
    while status == oh_behave.ExecuteResult.ready:
        status = billybob.execute()

main()
