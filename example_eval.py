import random

random.seed(3)

# number of additional exampls
n = 8
# examples from the ABS paper
paper_examples = [x-1 for x in [196693, 10071, 50160, 50730, 78090, 82007, 86828, 88158, 92908, 95188, 95758]]

example_line_numbers = []
for i in xrange(n):
    x = random.randint(0, 300000)
    example_line_numbers.append(x)
example_line_numbers = paper_examples + example_line_numbers
print example_line_numbers

with open('working_dir/example-eval.article.txt', 'wb') as of:
    with open('working_dir/test.article.txt') as af:
        with open('working_dir/test.title.txt') as tf:
            iat = []
            for i, (a, t) in enumerate(zip(af, tf)):
                if i in example_line_numbers:
                    iat.append((i, a, t))
            iat.sort(key=lambda x: example_line_numbers.index(x[0]))
            for i, a, t in iat:
                print i, 'I:', a
                print 'G:', t
                of.write(a)
