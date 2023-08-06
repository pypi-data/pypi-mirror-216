import unittest
from lark import Tree
from logictools.expression_parser import *
from logictools.logic_rule_transforms import *

'''
connective precedence when evaluating propositions.
1. Expressions in parentheses are processed (inside to outside)
2. Negation
3. And
4. Or
5. Implication
6. Biconditional
7. Left to right
'''


class TestExpressionManipulation(unittest.TestCase):
    
    def setUp(self) -> None:
        self.ep = ExpressionParser()
        self.tts = TreeToString()

    def test_expression_parser(self):
        with self.assertRaises(Exception):
            self.ep.parse('aVVb')
            self.ep.parse('av^b')
            self.ep.parse('(avb^c(')
            self.ep.parse('a<->(b->c)')  # valid expression, include in grammar?

        t1 = self.ep.parse('pv(qvq^v)^((qvq^p))<->(avb)^(avc)^(bvc)')
        self.assertIs(Tree, type(t1))

    def test_tree_to_string(self):
        ep = ExpressionParser()
        tts = TreeToString()
        tr = self.ep.parse('avbvc->b^dv(pvq^~r)<=>a')
        print(self.tts.transform(tr))

    def test_simplify_paren_expr(self):
        tr1 = self.ep.parse('((((a))))').children[0]
        tr2 = simplify_paren_expr(tr1)
        tr3 = self.ep.parse('((avb))').children[0]
        tr4 = simplify_paren_expr(tr3)
        print(tr2, self.tts.transform(tr4), sep="\n")

    def test_idempotence(self):
        ep = ExpressionParser()

        t1 = next(self.ep.parse('a^b^c^a^b^a').find_data('term'))
        t2 = next(self.ep.parse('a^b^c').find_data('term'))
        self.assertEqual(t2, idempotence(t1))

        t3 = next(self.ep.parse('(a^b^c)v(a^b^c)').find_data('term'))
        t4 = next(self.ep.parse('a^b^c').find_data('term'))
        self.assertEqual(t4, idempotence(t3))

    def test_reverse_idempotence(self):
        tr1 = self.ep.parse('p^q^r^s').children[0]
        tr2 = reverse_idempotence(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)v(c^b)').children[0]
        tr2 = reverse_idempotence(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_simplify_multiple_negation(self):
        tr1 = ExpressionParser().parse(
            '~~~a').children[0].children[0].children[0].children[0]
        tr2 = ExpressionParser().parse(
            '~~a').children[0].children[0].children[0].children[0]

    def test_identity(self):
        tr1 = self.ep.parse('avbvcvF').children[0]
        tr2 = self.ep.parse('a^b^c^T').children[0]

        print(tr1, tr2, sep="\n")
        print(identity(tr1), identity(tr2), sep="\n")

    def test_domination(self):
        tr1 = self.ep.parse('avbvcvT').children[0]
        tr2 = self.ep.parse('a^b^c^F').children[0]
        tr3 = self.ep.parse('a^b^c').children[0]

        print(tr1, tr2, sep="\n")
        print(domination(tr1), domination(tr2), domination(tr3), sep="\n")

    def test_commutativity(self):
        tr1 = self.ep.parse('a^b').children[0]
        tr2 = self.ep.parse('avbvc').children[0]
        print(commutativity(tr1), commutativity(tr2), sep="\n")

    def test_associativity_LR(self):
        tr1 = self.ep.parse('pv(qvr)vsv(tvu)vw').children[0]
        tr2 = associativity_LR(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)vr').children[0]
        tr2 = associativity_LR(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_associativity_expand(self):
        tr1 = self.ep.parse('(a^b)^(cvb)').children[0]
        tr2 = associativity_expand(tr1)
        tr3 = self.ep.parse('(a^b)vc').children[0]
        tr4 = associativity_expand(tr3)
        tr5 = self.ep.parse('av(bvc)vd^e').children[0]
        tr6 = associativity_expand(tr5)
        print(
            self.tts.transform(tr2),
            self.tts.transform(tr4),
            self.tts.transform(tr6),
            sep="\n")

    def test_reverse_associativity_expand(self):
        tr1 = self.ep.parse('pvqvrvs').children[0]
        tr2 = reverse_associativity_expand(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)v(c^b)').children[0]
        tr2 = reverse_associativity_expand(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_impl_to_disj(self):
        tr1 = self.ep.parse('p->q').children[0]
        tr2 = impl_to_disj(tr1)
        tr3 = self.ep.parse('p->q->p').children[0]
        tr4 = impl_to_disj(tr3)
        print(self.tts.transform(tr2), self.tts.transform(tr4), sep="\n")

    def test_dblimpl_to_impl(self):
        tr1 = self.ep.parse('p->q<=>~pvq').children[0]
        tr2 = dblimpl_to_impl(tr1)
        tr3 = self.ep.parse('p^q<=>q').children[0]
        tr4 = dblimpl_to_impl(tr3)
        print(self.tts.transform(tr2), self.tts.transform(tr4), sep="\n")

    def test_impl_to_dblimpl(self):
        tr1 = self.ep.parse('(p->q)^(q->p)').children[0]
        tr2 = impl_to_dblimpl(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(a->b)^(b->a)^c^(p->q)^(q->p)').children[0]
        tr2 = impl_to_dblimpl(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_negation(self):
        tr1 = self.ep.parse('pvq').children[0]
        tr2 = negation(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('~qvq').children[0]
        tr2 = negation(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('~p^q^p^q').children[0]
        tr2 = negation(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('~pvpvqv~qvr').children[0]
        tr2 = negation(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])

    def test_demorgan(self):
        tr1 = self.ep.parse('~(pvq)').children[0]
        tr2 = demorgan(tr1)
        tr3 = self.ep.parse('~(p^~q^r^~p)').children[0]
        tr4 = demorgan(tr3)
        tr5 = self.ep.parse('~p').children[0]
        tr6 = demorgan(tr5)
        print(
            self.tts.transform(tr2),
            self.tts.transform(tr4),
            self.tts.transform(tr6),
            sep="\n")

    def test_reverse_demorgan(self):
        tr1 = self.ep.parse('pv~qvr').children[0]
        tr2 = reverse_demorgan(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('a^b^~c').children[0]
        tr2 = reverse_demorgan(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_absorption(self):
        tr1 = self.ep.parse('(pvr)v(q^(pvr)^t)').children[0]
        tr2 = absorption(tr1)
        tr3 = self.ep.parse('p^(pvq)').children[0]
        tr4 = absorption(tr3)
        tr5 = self.ep.parse('pv(q^r)').children[0]
        tr6 = absorption(tr5)
        print(self.tts.transform(tr2), tr4, self.tts.transform(tr6), sep="\n")

    def test_reverse_absorption(self):
        tr1 = self.ep.parse('p').children[0]
        tr2 = reverse_absorption(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)').children[0]
        tr2 = reverse_absorption(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_literal_negation(self):
        tr1 = self.ep.parse('~F').children[0]
        tr2 = TF_negation(tr1)
        tr3 = self.ep.parse('~T').children[0]
        tr4 = TF_negation(tr3)
        tr5 = self.ep.parse('~~F').children[0]
        tr6 = TF_negation(tr5)
        print(tr2, tr4, tr6, sep="\n")

    def test_distributivity(self):
        tr1 = self.ep.parse('pv(q^r)').children[0]
        tr2 = distributivity(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('~qv(qvr)').children[0]
        tr2 = distributivity(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(~p^q)^r').children[0]
        tr2 = distributivity(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('pvqv(p^r)v(s^r)').children[0]
        tr2 = distributivity(tr1)
        print([t if type(t) == Token else self.tts.transform(t) for t in tr2])

    def test_reverse_distributivity(self):
        tr1 = self.ep.parse('(pvq)^(pvr)^(qvr)^(pvrvs)^(avb)^(avc)').children[0]
        tr2 = reverse_distributivity(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)^(rvq)').children[0]
        tr2 = reverse_distributivity(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(pvq)^(pvr)').children[0]
        tr2 = reverse_distributivity(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('(r^q)^(p^r)').children[0]
        tr2 = reverse_distributivity(tr1)
        print([self.tts.transform(t) for t in tr2])
        tr1 = self.ep.parse('pvq').children[0]
        tr2 = reverse_distributivity(tr1)
        print([self.tts.transform(t) for t in tr2])

    def test_double_negate(self):
        tr1 = self.ep.parse('p^(pvq)').children[0]
        tr2 = double_negate(tr1)
        tr3 = self.ep.parse('p')  # is this correct?
        tr4 = double_negate(tr3)
        tr5 = self.ep.parse('(p^(q^r))').children[0]
        tr6 = double_negate(tr5)
        print(
            self.tts.transform(tr2),
            self.tts.transform(tr4),
            self.tts.transform(tr6),
            sep="\n")


if __name__ == "__main__":
    unittest.main()
