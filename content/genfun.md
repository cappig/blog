---
title: Fun with generating functions
description: Playing around with an elegant mathematical tool
date: 2025-09-29
---

![clothesline](/static/img/article/wash_line.jpeg)*"A generating function is a clothesline on which we hang up a sequence of numbers for display" -- Herbert Wilf, [Generatingfunctionology](https://www2.math.upenn.edu/~wilf/gfology2.pdf)*
{: .img_box }


## Counting bills

Consider the following problem:
> You have an unlimited number of $1, $5, and $10 bills. How many ways are there to make $10?

Let’s work it out: we could use ten $1 bills, five $1 bills, and one $5 bill, two $5 bills, or a single $10 bill. That gives us four possible ways. While this works for small numbers, it quickly becomes tedious as the number of bills and denominations increases. Can we find a more systematic method, one that also generalizes to larger cases?

Let’s examine the problem again. Note that each denomination contributes some multiple of its value, so we can only possibly choose a set number of bills of each denomination. For $1 bills, we can take 0, 1, 2, or any other number up to 10; for $5 bills, we can take 0, 1, or 2, and for $10 bills, we can only take 0 or 1.

So we have to find the number of valid combinations of these bills. Is there a way to _encode_ these values so that they can be easily manipulated and the answer easily extracted? One seemingly random way to do this is to use polynomials. Let the exponent track the total sum and the coefficient track the number of ways to achieve that sum. So, for example, \\(4 x^{12}\\) would mean that there are 4 ways to add up our bills to get the value 12.

For the $1 bill, we construct the polynomial \\(1 + x + \dots + x^{10}\\) because we can achieve any sum by just choosing that number or $1 bills. For the $5 bill we have \\(1 + x^5 + x^{10}\\), and similarly for the $10 bills we have \\(1 + x^{10}\\). Note the presence of \\(x^0\\) (1), this is because we can always choose zero of a given denomination.

Let's multiply these three polynomials together and see what we get:
$$ (1 + x + \dots + x^{10}) \cdot (1 + x^5 + x^{10}) \cdot (1 + x^{10}) \\\\ = 1 + x + x^2 + x^3 + x^4 + 2x^5 + 2x^6 + 2x^7 + 2x^8 + 2x^9 + 4x^{10}. $$

Notice that the coefficient next to \\(x^{10}\\) is 4, --- our desired answer! Not only that, now we also know how many ways the sums from 1 to 9 can be achieved!

It turns out the multiplication of polynomials models the way we choose bill combinations in this problem, and in general, it models the way we form subsets in similar combinatorial problems.

In this case this doesn't really save us much work, but this principle can help crack many hard problems. Generating functions are one of those mathematical tools that has to be used to be understood, it feels a bit contrived, but it works extremely well in practice. This introductory problem is a good way to grasp the basics but there is a lot more to generating functions!

<details markdown="1">
<summary markdown="1">*Extra: closed form solution to this problem*</summary>
This problem of 'counting bills' actually has a closed form solution! The solution doesn't directly involve generating functions, but they can be used to help deduce the initial equation[^bills_equ]. But it is still fun nonetheless, so I include it here as an extra.

Let  \\(a\\), \\(b\\) and \\(c\\) be the number of $1, $5, and $10 bills, respectively. Then the number of ways to sum to \\(k\\) dollars will be the number of nonnegative integer solutions of the expression
$$ a+5b+10c = k.$$

1. Let's first fix \\(c\\). Notice that \\(0 \leq c \leq \left\lfloor \frac{k}{10} \right\rfloor \\) must hold. Let's define \\(k' = k - 10c \\) thus giving us \\(a + 5b = k'\\).
2. Let's now fix \\(b\\). Notice that now \\(0 \leq b \leq \left\lfloor \frac{k'}{5} \right\rfloor \\) must also hold. So we get \\(a = k' - 5b \\).
3. We can see that \\(a\\) depends solely on the choice of \\(b\\) so we have one choice of \\(a\\) for each choice of \\(b\\). The number of  choices for \\(b\\) is \\(\left\lfloor \frac{k'}{5} \right\rfloor + 1\\). The \\(+1\\) here accounts for the choice of zero bills.

Expanding this expression, we get the number of choices for \\(b\\) as
$$ \left\lfloor \frac{k - 10c}{5} \right\rfloor + 1. $$

We also have to account for \\(c\\), so since \\(b\\) depends on \\(c\\), we get the final expression for the number of choices that sum to \\(k\\) as
$$ c_k = \sum_{c=0}^{\lfloor k/10 \rfloor} \left(\left\lfloor \frac{k-10c}{5} \right\rfloor + 1 \right). $$

We can turn this into a closed form by first noting that \\( \left\lfloor \frac{k-10c}{5} \right\rfloor = \left\lfloor \frac{k}{5} \right\rfloor - 2 c\\) (here the floor around \\(2 c\\) vanishes due to \\(c\\) always being an integer). We can then expand the sum
$$\begin{align\*} c_k &= \sum_{c=0}^{\lfloor k/10 \rfloor} \left(\left\lfloor \frac{k}{5} \right\rfloor + 1 - 2 c \right) \\\\ &= \left( \left\lfloor \frac{k}{10} \right\rfloor + 1 \right) \left( \left\lfloor \frac{k}{5} \right\rfloor + 1 \right) - 2  \sum_{c=0}^{\lfloor k/10 \rfloor} c \\\\ &= \left( \left\lfloor \frac{k}{10} \right\rfloor + 1 \right) \left( \left\lfloor \frac{k}{5} \right\rfloor + 1 \right) - \cancel{2} \frac{\left\lfloor \frac{k}{10} \right\rfloor \left( \left\lfloor \frac{k}{10} \right\rfloor + 1\right)}{\cancel{2}}. \end{align\*} $$

We can factor the last expression and get the following closed form[^closed_form] expression
$$ c_k = \left( \left\lfloor \frac{k}{10} \right\rfloor + 1 \right) \left( \left\lfloor \frac{k}{5} \right\rfloor + 1 - \left\lfloor \frac{k}{10} \right\rfloor \right). $$
</details>


## Fibonacci numbers

One of the most famous integer sequences in mathematics is the [Fibonacci sequence](https://en.wikipedia.org/wiki/Fibonacci_sequence) ([A000045 in the OEIS](https://oeis.org/A000045)). It gets its name from the Italian mathematician [Leonardo of Pisa](https://en.wikipedia.org/wiki/Fibonacci), known commonly as Fibonacci, who described them in his 1202 book [Liber Abaci](https://en.wikipedia.org/wiki/Liber_Abaci). Latin for "The Book of Calculation", it also introduced, among other things, the [Hindu–Arabic base 10 numerals](https://en.wikipedia.org/wiki/Hindu%E2%80%93Arabic_numeral_system) to Europe. But this sequence has been known to humans for a lot longer than that, first appearing in the writings of [Indian mathematicians](https://en.wikipedia.org/wiki/Indian_mathematics#Pingala_(300_BCE_%E2%80%93_200_BCE)) around 200 BCE.

![liber abaci page](/static/img/article/liber_abaci.jpg)*A page from Liber Abaci containing the Fibonacci sequence in the right margin. Note the use of Arabic and Hindu numerals in red.*
{: .img_box }

A given element in the Fibonacci sequence is defined as the sum of the two preceding elements, where the first two elements are given as 0 and 1. This can be expressed with the following recurrence relation
$$ F_0 = 0, \\ F_1 = 1 \\\\ F_n = F_{n-1} + F_{n-2}, \quad n > 1. $$

Its first few members are:
$$ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ... $$

But what if we want to know, say, the 200th Fibonacci number? Would we have to solve the recurrence relation 200 times? It turns out that we don't, because we can construct a closed-form formula for the \\(n\\)-th Fibonacci number! This can be done using generating functions!

This is because, essentially, a generating function is a way to represent an infinite sequence as the coefficients of a [formal](https://en.wikipedia.org/wiki/Formal_power_series) power series. Since the series is formal, we are not concerned with its convergence, and the variable \\(x\\) is an [indeterminate](https://en.wikipedia.org/wiki/Polynomial_ring). So the infinite sequence \\( ( a_0, a_1, a_2, ...) \\) can be expressed with the generating function \\( \sum_{n=0}^{\infty} a_n x^n  = a_0 + a_1 x + a_2 x^2 + \cdots \\). For example the sequence \\( (1, 1, 1, ...) \\) has \\( \sum_{n=0}^{\infty} x^n = \frac{1}{1-x} \\) as it's generating function. Note that we can use the closed form of the series to represent the generating function.

Generating functions defined this way---as the coefficients of a geometric series---are called _ordinary generating functions_. There are [many kinds](https://en.wikipedia.org/wiki/Generating_function#Types) of generating functions; I might mention some more in a future article. Each of them helps us solve a specific class of problems.

OK, back to the Fibonacci sequence. Let's start by defining its generating function as
$$ G(x) = \sum_{n=0}^{\infty} F_n x^n . $$

Now recall the recurrence relation given above. We can use it to rewrite the series and get
$$ \begin{align\*} G(x) &= F_0 + F_1 x + \sum_{n=2}^{\infty} F_n x^n \\\\ &= 0 + 1 x + \sum_{n=2}^{\infty} (F_{n-1} + F_{n-2}) x^n \\\\ &= x + x \sum_{n=2}^{\infty} F_{n-1} x^{n-1} + x^2 \sum_{n=2}^{\infty} F_{n-2} x^{n-2}. \end{align\*} $$

We can now take care of the sums. Since \\( F_0 = 0 \\) the first sum becomes \\( 0 + x \sum_{n=1}^{\infty} F_{n-1} x^{n-1} \\). So by shifting indices both sums become \\(  \sum_{n=0}^{\infty} F_n x^n \\). This is just our generating function! So substituting that in gives us the expression
$$ G(x) = x + x G(x) + x^2 G(x). $$

After factoring out \\( G(x) \\) we get
$$ G(x) = \frac{x}{1-x-x^2}. $$

At this point we could actually just take the [Maclaurin series](https://en.wikipedia.org/wiki/Maclaurin_series) expansion of the above function to get each Fibonacci number. This is also interesting in itself but we want a closed form formula. So to continue we can use partial fraction decomposition to simplify the expression.

Let's start by solving \\( -x^2 - x + 1 = 0 \\). We can plug the parameters into the quadratic equation to get the two roots
$$ \phi = \frac{1 + \sqrt{5}}{2}, \\ \psi = \frac{1 - \sqrt{5}}{2}. $$

Now continuing with the partial fraction decomposition, we get
$$ G(x) = \frac{x}{(1 - \phi x)(1 - \psi x)} = \frac{A}{1 - \phi x} + \frac{B}{1 - \psi x}. $$

After some fairly easy algebra we can conclude that \\( A = \frac{1}{\sqrt{5}} \\) and \\( B = - \frac{1}{\sqrt{5}} \\). Substituting that in, and noting that \\( \sum_{n=0}^{\infty} (a x)^n = \frac{1}{1 - ax} \\) we get the following expression
$$\begin{align\*} G(x) &= \frac{1}{\sqrt{5}} \left( \frac{1}{1 - \phi x} - \frac{1}{1 - \psi x} \right) \\\\ &= \frac{1}{\sqrt{5}} \left( \sum_{n=0}^{\infty} ( \phi x )^n -  \sum_{n=0}^{\infty} ( \psi x )^n \right) \\\\ &= \sum_{n=0}^{\infty} \frac{\phi^n - \psi^n}{\sqrt{5}} x^n. \end{align\*} $$

Since the coefficients of \\( G(x) \\) are the Fibonacci numbers \\( F_n \\) we now have the final closed form
$$ F_n = \frac{\phi^n - \psi^n}{\sqrt{5}} = \frac{1}{\sqrt{5}} \left( \left( \frac{1 + \sqrt{5}}{2} \right)^n - \left( \frac{1 - \sqrt{5}}{2} \right)^n \right). $$

This expression is known as [Binet's formula](https://en.wikipedia.org/wiki/Fibonacci_sequence#Binet's_formula), and generating functions aren't the only way to derive it. But this procedure demonstrates how useful and surprisingly versatile they are.

<details markdown="1">
<summary markdown="1">*Extra: connection to the golden ratio*</summary>
You might have noticed that the roots of the quadratic polynomial we solved during partial fraction decomposition are actually the [golden ratio](https://en.wikipedia.org/wiki/Golden_ratio) \\( \phi \\) and its conjugate \\( \psi = - \frac{1}{\phi} \\).

The connection between Fibonacci numbers and the golden ratio is very well known. It's perhaps one of the most famous 'math facts' presented in pop science. This connection is due to the fact that
$$ \lim_{n \to \infty} \frac{F_{n+1}}{F_n} = \phi. $$

This is not hard to prove if we have a formula for \\(F_n\\). Doing some simple algebra yields
$$ \lim_{n \to \infty} \frac{F_{n+1}}{F_n} = \lim_{n \to \infty} \frac{\phi^{n+1}-\psi^{n+1}}{\phi^n - \psi^n} = \lim_{n \to \infty} \frac{\phi - \psi\left(\frac{\psi}{\phi}\right)^{n}}{1- \left(\frac{\psi}{\phi}\right)^n}. $$

Now note that \\(\left| \frac{\psi}{\phi} \right| < 1 \implies \lim_{n \to \infty} \left( \frac{\psi}{\phi} \right)^n = 0 \\). Thus giving us our final result
$$ \lim_{n \to \infty} \frac{\phi - \cancel{\psi\left(\frac{\psi}{\phi}\right)^{n}}}{1 - \cancel{\left(\frac{\psi}{\phi}\right)^n}} = \phi. $$

While the golden ratio has some [interesting mathematical properties](https://en.wikipedia.org/wiki/Golden_ratio#Mathematics), a lot of the things [claimed](https://en.wikipedia.org/wiki/Golden_ratio#Disputed_observations) about it are unfortunately tantamount to numerology.
</details>


## Counting trees

Now let's take a walk in the mathematical forest. This forest is made up of [binary trees](https://en.wikipedia.org/wiki/Binary_tree) --- a type of [graph](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) commonly used in computer science. They are rooted, and each tree node has at most 2 children.

![a binary tree in real life](/static/img/article/irl_binary_tree.jpg)*Hyphaene compressa[^tree] would probably be in our forest. This specimen is a full binary tree with 31 nodes.*
{: .img_box }

We may want to know how many ways there are to construct such a tree with \\(n\\) nodes. Like any combinatorial problem, the best way to solve it is to draw out the first few cases to see if we notice a pattern.

![binary tree constructions](/static/img/article/binary_trees.svg)*All possible ways to construct binary trees with 1, 2, and 3 nodes.*
{: .img_box }

Note that for 0 nodes there is 1 way to construct an empty tree. Note also that we treat the right and left child as distinct.

After drawing out these trees for a while, you might notice that this problem becomes a bit recursive. The easiest way to construct new trees is to take the trees from the previous level and add new branches.

We can generalize this thinking if we consider only the root node of a tree with \\(n\\) nodes. It has a left subtree with \\(0 \leq k \leq n-1\\) nodes, and a right subtree with \\(n-1-k\\) nodes. We can then apply the [rule of product](https://en.wikipedia.org/wiki/Rule_of_product) and conclude that for a given \\(k\\) there are \\(C_{k} \cdot C_{n-1-k}\\) such trees.

Summing over all possible values of \\(k\\), we get the following recurrence relation
$$ C_n = \sum_{k=0}^{n-1} C_{k} C_{n-1-k}, \quad n \geq 1. $$

As stated above, our initial condition is \\(C_0=1\\). You can start plugging numbers in and verify that this lines up with the number of graphs we got earlier. This is nice and useful, but we want the coveted closed-form expression. This can be achieved using, you guessed it, generating functions!

Let \\(C(x) = \sum_{n=0}^{\infty} C_n x^n\\) be the generating function of this sequence. Plugging the recurrence relation we just derived into it yields
$$\begin{align\*} \sum_{n=1}^{\infty} \left(\sum_{k=0}^{n-1} C_k C_{n-1-k}\right) x^n &= \sum_{n=1}^{\infty} C_n x^n \\\\ &= \sum_{n=0}^{\infty} C_n x^n - C_0 \\\\ &= C(x) - 1. \end{align\*}$$

Now, doesn’t the sum on the left look a bit familiar? It looks very similar to the formula for the [discrete convolution](https://en.wikipedia.org/wiki/Convolution#Discrete_convolution) of two infinite series, or the [Cauchy product](https://en.wikipedia.org/wiki/Cauchy_product): \\( ( \sum_{i=0}^{\infty} a_{i} ) \cdot ( \sum_{j=0}^{\infty} b_{j} ) = \sum_{k=0}^{\infty} \left( \sum_{l=0}^{k} a_{l} b_{k-l} \right) \\). But for this to be an actual Cauchy product \\(n\\) would need to start from 0. We can fix this by letting \\(m=n-1\\) and factoring out \\(x\\)
$$\begin{align\*} \sum_{n=1}^{\infty} \left(\sum_{k=0}^{n-1} C_k C_{n-1-k}\right) x^n &= x \sum_{n=1}^{\infty} \left(\sum_{k=0}^{n-1} C_k C_{n-1-k}\right) x^{n-1} \\\\ &= x \sum_{m=0}^{\infty} \left(\sum_{k=0}^{m} C_k C_{m-k}\right) x^m \\\\ &= x \left(\sum_{n=0}^{\infty} C_n x^n\right) \left(\sum_{n=0}^{\infty} C_n x^n\right) \\\\ &= x C(x)^2. \end{align\*}$$

This demonstrates another powerful feature of generating functions: multiplication of generating functions yields the discrete convolution of their sequences. Another reason why they prove so useful in solving combinatorial problems, where convolutions show up regularly.

Continuing with the problem, we can now put the two sides together to get
$$ C(x) - 1 = x C(x)^2.$$

This is a quadratic equation in \\(C(x)\\). After once again using the trusty quadratic formula, we get
$$ C(x) = \frac{1 \pm \sqrt{1 - 4x}}{2x}. $$

Now you might notice a problem here, the real domain of this function is \\( \left(-\infty, \frac{1}{4}\right] \\). This is due to the square root, which is real only for \\( x \leq \frac{1}{4} \\). Ah, but remember that this is a generating function, so we don't care about the numerical value of \\( C(x) \\), we only want the coefficients of its power series.

But we still have two possible branches. How do we choose the correct branch? Well, we know that \\(C_0 = 1\\), that is just our initial condition. And we know that we can also extract coefficients using the Maclaurin expansion \\( C_n = \frac{C^{(n)}(0)}{n!} \\). So it follows that \\( C_0 = C(0) \\). But our formula has division by zero, so we have to take the limit where \\( x \to 0 \\). Doing this for both branches gives us
$$ \begin{align\*} \lim_{x \to 0} \frac{1 + \sqrt{1 - 4x}}{2x} &= \frac{1+1}{0} = +\infty \\\\ \lim_{x \to 0} \frac{1 - \sqrt{1 - 4x}}{2x} &\overset{\mathrm{L'H}}{=} \lim_{x \to 0} \frac{2 (1 - 4x)^{-\frac{1}{2}}}{2} = 1. \end{align\*}$$

So we can reject the \\(+\\) branch, and see that the \\(-\\) branch is the one that produced the desired result. Now we want to get a formula for the \\(n\\)-th coefficient of the power series expansion of this expression.

Starting with the [binomial series](https://en.wikipedia.org/wiki/Binomial_series) \\( \sum_{n=0}^\infty \binom{\alpha}{n} x^n = (1 + x)^\alpha \\), we can expand the radical to get \\( (1-4x)^{\frac{1}{2}}= \sum_{k=0}^\infty \binom{\frac{1}{2}}{k}(-4x)^k \\). The 0-th coefficient of this series is 1, so the numerator gets expanded to \\( 1- (1-4x)^{\frac{1}{2}}= -\sum_{k=1}^\infty \binom{\frac{1}{2}}{k}(-4x)^k \\). Dividing this by \\(2x\\) and reindexing with \\(n=k-1\\) gives us the expansion
$$\begin{align\*} C(x) = \frac{1 - \sqrt{1 - 4x}}{2x} &= -\frac{1}{2} \sum_{k=1}^\infty \binom{\frac{1}{2}}{k}(-4)^k x^{k-1} \\\\  &= -\frac{1}{2} \sum_{n=1}^\infty \binom{\frac{1}{2}}{n+1}(-4)^{n+1} x^{n}, \end{align\*} $$

So there we have it, the closed-form expression for our problem is
$$ C_n = -\frac{1}{2} \binom{\frac{1}{2}}{n+1}(-4)^{n+1}. $$

But yeah, this is way too ugly... Let's try to simplify it! The most obvious place to start is \\( \binom{\frac{1}{2}}{n+1} \\).

We usually define the binomial coefficients like \\( \binom{a}{b} = \frac{a!}{b! (a-b)!} \\). This won't work in our case since \\(a\\) is not an integer, and thus \\(a!\\) is not defined[^gamma].

To fix this let's introduce the [falling factorial](https://en.wikipedia.org/wiki/Falling_and_rising_factorials) \\( a^{\underline{b}} = a (a-1) \cdots (a - (b-1)) \\). Now it obviously follows that \\( a^{\underline{b}} = \frac{a!}{(a-b)!} \\). Plugging this into the definition of the binomial coefficient, we get \\( \binom{a}{b} = \frac{a^{\underline{b}}}{b!} \\). Applying this to our coefficient, we have
$$ \binom{\frac{1}{2}}{n+1} = \frac{(\frac{1}{2})^{\underline{n+1}}}{(n+1)!} = \frac{\frac{1}{2} (\frac{1}{2} - 1) \cdots (\frac{1}{2} - (n+1 -1))}{(n+1)!}. $$

We can factor out \\(\frac{1}{2}\\) from each parenthetical and get
$$ \frac{\frac{1}{2} \frac{1}{2^n} (1 - 2) (1 - 4) \cdots (1 - 2n)}{(n+1)!} = \frac{(\frac{1}{2})^{n+1} \prod_{k=1}^n (1 - 2k)}{(n+1)!}. $$

Now, thinking ahead for a bit, we can factor -1 from the product so that it cancels out the -4 in the whole expression. We now have
$$ \binom{\frac{1}{2}}{n+1} = \frac{(-1)^n \prod_{k=1}^n (2k - 1)}{2^{n+1} (n+1)!.} $$

We can now plug this expression into the full formula for \\(C_n\\), after canceling out a bunch of stuff, we get
$$\begin{align\*} C_n &= (-1)^{n+1} (-4)^{n+1} \; \frac{1}{2} \frac{1}{2^{n+1}} \frac{\prod_{k=1}^n (2k - 1)}{(n+1)!} \\\\ &= \cancel{(-1)^{n+1}} \cancel{(-1)^{n+1}} \; \frac{2^{2n+2}}{2^{n+1+1}} \frac{\prod_{k=1}^n (2k - 1)}{(n+1)!} \\\\ &= \frac{\cancel{2^{n+2}}}{\cancel{2^{n+2}}} \; 2^n \frac{\prod_{k=0}^n (2k - 1)}{(n+1)!} \\\\ &= 2^n \frac{\prod_{k=1}^n (2k - 1)}{(n+1)!}. \end{align\*} $$

But we still have this cumbersome product in the numerator. Perhaps there is a way to write it in a closed form?

Consider \\((2n)! = \prod_{k=1}^{2n} k\\). We can split the even and odd parts to get \\( (2n)! = \prod_{k=1}^n (2k)(2k-1) \\). Now let's look at the even part of this expression \\( \prod_{k=1}^n 2k = 2n (2n-2) \cdots 2\\), notice that we can factor out 2 and then be left with \\(n!\\), like so \\( \prod_{k=1}^n 2k = 2^n n!\\). And now, putting this together, we can express our product like
$$ \prod_{k=1}^n (2k-1) = \frac{(2n)!}{2^n n!}. $$

This is actually a well-known identity! See the product \\( \prod_{k=1}^n (2k - 1)\\) can be written as a [double factorial](https://en.wikipedia.org/wiki/Double_factorial). The double factorial \\(n!!\\) is defined as the product of all positive integers up to \\(n\\) that have the same parity as \\(n\\). In this case, we write it as \\( (2n-1)!! \\) which is always the product of odd numbers, giving us a nice product with simple bounds. Double factorials show up quite commonly in combinatorics, so this is a useful thing to know.

We’re in the final stretch now. We can plug this into our formula for \\(C_n\\), doing that yields
$$ C_n = \frac{\cancel{2^n} (2n)!}{\cancel{2^n} n! (n+1)!} = \frac{1}{n+1} \binom{2n}{n}. $$

Phew, so there we are. A nice closed-form expression for our tree-counting problem. Well, not just the tree-counting problem... This expression generates the sequence:
$$ 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, \dots $$

This sequence ([A000108 in the OEIS](https://oeis.org/A000108)) is quite special; its members are called the [Catalan numbers](https://en.wikipedia.org/wiki/Catalan_number). They get their name from [Eugène Charles Catalan](https://en.wikipedia.org/wiki/Eug%C3%A8ne_Charles_Catalan), a 19th-century Belgian mathematician, but they were described much earlier by the Mongolian mathematician [Minggatu](https://en.wikipedia.org/wiki/Minggatu) in the 1730s and [Leonhard Euler](https://en.wikipedia.org/wiki/Leonhard_Euler) in 1751.

What makes this sequence special is the fact that it shows up so commonly in combinatorics. For the sake of brevity, I will just list out the most famous ones:

* The number of legal ways to arrange \\(n\\) sets of parenthesis. This is directly equivalent to the number of possible [Dyck words](https://en.wikipedia.org/wiki/Dyck_language) of length \\(2n\\).
* The number of ways to triangulate a convex \\((n+2)\\)-gon. This is the way Euler discovered Catalan numbers.
* The number of ways to construct a full binary tree with \\(n+1\\) labeled leaves.
* The number of [noncrossing partitions](https://en.wikipedia.org/wiki/Noncrossing_partition) of the set of \\(n\\) elements.
* The number of ways to form a “mountain range” with n up-strokes and n down-strokes that all stay above the original line.
* The number of paths on a \\(n \times n \\) square grid from bottom to top that do not cross the main diagonal.

![all possible Catalan paths on a 4x4 grid](/static/img/article/catalan_paths.svg)*All possible ways to construct these paths on a \\(4 \times 4\\) grid. If we count them, we get 14 --- the 4th Catalan number!*
{: .img_box }

There are many, many more. Wikipedia [lists](https://en.wikipedia.org/wiki/Catalan_number#Applications_in_combinatorics) a couple more, and [Richard P. Stanley's](https://en.wikipedia.org/wiki/Richard_P._Stanley) definitive monograph [Catalan Numbers](http://www.cambridge.org/9781107427747) has some 200 pages worth of dense information on this one sequence. Stanley also produced some [slides](https://math.mit.edu/~rstan/transparencies/miami_catalan.pdf) that summarize this topic and elucidate some of the examples given above.


### Conclusion

This is only the tip of the iceberg when talking about generating functions. They are a really fascinating mathematical tool that is both fun and useful. I'll probably write another article about them.

Catalan numbers are also a fascinating topic on their own. I believe that the OEIS entry about them is the longest one on the entire site! They really are that special.

#### Literature

For generating functions, there really is no book better than [generatingfunctionology](https://www2.math.upenn.edu/~wilf/gfology2.pdf) by [Herbert Wilf](https://en.wikipedia.org/wiki/Herbert_Wilf). It is _the_ book about generating functions, and it has the best name of any math book I know of. For Catalan numbers, I have already recommended Stanley's [Catalan Numbers](http://www.cambridge.org/9781107427747).

As always, 3Blue1Brown has an excellent [video](https://www.youtube.com/watch?v=bOXCLR3Wric) on generating functions. SackVideo also has a good [video](https://www.youtube.com/watch?v=dLiT9axMDrg) on the topic, focusing more on the problem of counting binary trees.


Well, that's it for this entry! Have fun and happy hacking!



[^tree]: Image attribution: `© C. Godfray; © John Dransfield, Royal Botanic Gardens, Kew`. It can be found on [palmweb.org](https://www.palmweb.org/cdm_dataportal/taxon/e4e041df-ab26-4abb-a507-08bec2f14b83/images)
[^gamma]: We could use the [gamma function](https://en.wikipedia.org/wiki/Gamma_function) to extend the domain of the factorial to all real numbers, but here that wouldn't help us to simplify the whole expression.
[^bills_equ]: Since \\(\left( \sum_{n=0}^\infty x^n \right) \cdot \left( \sum_{n=0}^\infty x^{5n} \right) \cdot \left( \sum_{n=0}^\infty x^{10n}\right)\\) is the generating function for our problem we can derive the expression for the \\(k\\)-th coefficient \\(c_k\\) by using the [Cauchy product](https://en.wikipedia.org/wiki/Cauchy_product). It is not hard to show that for these three sums this becomes \\(c_k = \sum_{a+5b+10c=k} 1\\), thus landing us at the same spot as before --- looking for the number of nonnegative integer solutions to \\(a+5b+10c=k\\).
[^closed_form]: Whether expressions containing floor functions count as closed form is debatable, but since 'closed form expression' doesn't have a strict definition, I will consider these expressions to count here.
