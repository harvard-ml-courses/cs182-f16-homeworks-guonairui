import sys
sys.dont_write_bytecode = True
from hw5 import TextClassifier

def test(o, e, val = 1, tol=.01):
    if type(o) is list:
        err = 0
        for i in xrange(len(o)):
            err += float(abs(o[i]-e[i])) / (e[i] + .000000000000000001)
        tol *= len(o)
    else:
        err = float(abs(o-e)) / (e + .000000000000000001)
    if err < tol:
        global points
        points += val
        return str(val) + "/" + str(val)
    else:
        return str(0) + "/" + str(val)

points = 0
cut = TextClassifier()
ans = cut.q0()
if type(ans) is str: ans = [ans]
print len(ans), "collaborators on this assignment (include all names in a list)"

ans = cut.q1()
print "q1 looks like probabilities", test(sum(ans), 1, .1)
print "q1 is correct", test(ans, [8./20, 4./20, 2./20, 6./20], .1)

ans = cut.q2()
print "q2 looks like probabilities", test(sum(ans), 1, .1)
print "q2 is correct", test(ans, [10./28, 6./28, 4./28, 8./28], .2)

ans = cut.q3([8,4,2,6])
print "q3 looks like probabilities", test(sum(ans), 1, .1)
print "q3 is correct", test(ans, [8./20, 4./20, 2./20, 6./20], .4)

print "#### MINI ####"
cut.q4('mini.train')
print "Right number of words:", len(cut.dict) == 8, "and ratings:", sum(cut.nrated) == 5
cut.q5()
print "q5 generates right F:", test(sum(cut.F, []), [2.01, 2.01, 2.71, 2.71, 2.01, 2.71, 2.01, 1.32, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 1.5, 1.95, 1.95, 2.64, 2.64, 1.95, 1.95, 1.95, 1.95, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 1.5, 1.79, 1.79, 1.79, 1.79, 2.48, 2.48, 2.48, 2.48])
ans = cut.q6('mini.valid')
print "q6 has right predictions:", test(ans[0], [4, 0, 2], 1)
print "q6 has right accuracy:", test(ans[1], 1./3, 1)
alpha = cut.q7('mini.valid')
cut.q5(alpha)
ans = cut.q6('mini.valid')
print "q7 produces better accuracy:", test(int(ans[1] >= 1./3 and alpha != 1), 1, 2)
cut.q5()
ans = cut.q8()
print "q8 hallucinates right words:", test(int(ans[2][0] == 'not' and ans[4][2] in ['182', 'cs'] and set(['rocks', '!']) == set(ans[4][:2]) and ans[0][0] == '.'), 1, 2)

print "#### STSA ####"
cut.q4('stsa.train')
print "Right number of words:", len(cut.dict) == 16581, "and ratings:", sum(cut.nrated) == 8544
cut.q5()
ans = cut.q6('stsa.valid')
print "q6 has right accuracy:", test(ans[1], 0.3851, 1)
ans = cut.q6('stsa.test')
print "q6 has right accuracy:", test(ans[1], 0.4014, 2)
alpha = cut.q7('stsa.valid')
cut.q5(alpha)
ans = cut.q6('stsa.valid')
print "q7 produces better accuracy:", test(int(ans[1] > 0.3851 and alpha != 1), 1, 2)
cut.q5()
ans = cut.q8()
print "q8 hallucinates right words:", test(int(ans[0][0] == 'incoherent' and ans[1][0] == 'sadly' and 'diversion' in ans[3][:2] and ans[4][0] == 'captivating' and ans[4][1] == 'splendid'), 1, 2)

print int(points), "out of 15 points received"
