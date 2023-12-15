Title: DSPy Assertions: A Program Synthesis Perspective
Date: 2023-12-15 6:31
Category: Research
Tags: DSPy, LLM, Assertions, Program Recovery, Program Synthesis, PL
Description: Deep connections between traditional program synthesis and self-refining LM programs with assertions.
Status: Published

<section markdown="1">

Prompting and its engineering first emerged as a way of interacting with LMs due to 
chat being the primary application of LMs. It involves brittle and error-prone natural language statements used to guide the LM to a desired output.

However, for many tasks, more context aware models could skip chatting altogether. That leads us to the question: **how can we program LMs without prompting?**


Language model (LM) programs are a programming paradigm that
combines the precision of conventional programming with the flexibility of
LMs. [DSPy](https://github.com/stanfordnlp/dspy) is a framework for creating such programs declaratively, with automatic prompt tuning through compilation.
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
  This [short blog](https://arnavsinghvi11.github.io/posts/2023/10/6/blog-post/) summarizes how DSPy works in a nutshell. You can try DSPy in this free [Colab](https://colab.research.google.com/github/stanfordnlp/dspy/blob/main/intro.ipynb).
</span>
Let's build a simple ubercool LM program.

### PR Reviewer with DSPy 

This program reviews a github pull request:

```python
class Reviewer(dspy.Module):
  def __init__(self):
    self.gen_review = dspy.ChainOfThought("pull_request -> review, status")

  def forward(self, pr):
    return self.gen_review(pull_request=pr)
```

You could use this program as follows:
```python

reviewer = Reviewer()
result = reviewer(pr="def add(a, b): return a + b")
print(result.review, result.status)

# review: ... could be improved by renaming 
# the function and adding proper error handling.
# status: Changes requested
```

DSPy also automatically compiles quality few-shot prompts for your program, so you don't have to! You can use it to build a more robust reviewer in a few lines and some I/O pairs.
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    In the code, `is_valid` is the optimizer metric and could be a fuzzy string match or an LLM call that checks the review's validity.
</span>
```python
teleprompter = BootstrapFewShot(metric=is_valid)
reviewer = teleprompter.compile(Reviewer(), trainset=io_pairs)
```
</section>

<section markdown="1">

## Reflection: Is this a good reviewer? 🤔

<img src="./images/lgtm.jpeg" alt="drawing" width="200" style="float: right; border: dashed;"/>
It is relatively easy to write a valid review for a PR. 

But, a good reviewer is writes _concise_, _constructive_, and _informative_ reviews. The question is, __how do we capture and ensure these properties in a program?__

</section>


<section markdown="1">

## "Sketching" the Solution (pun intended)

In traditional program synthesis, particularly in the context of sketching, developers provide a high-level outline of a program— a __sketch__—along with a set of __assertions__ that specify the desired behavior. The synthesizer then fills in the details, turning the sketch into a fully-fledged program that adheres to the assertions.

<blockquote markdown="1">
Assertions in a sketch allow expresssing intuitive insights 
without having to think too much about the details of the implementation.
</blockquote>

By now, one might see that DSPy is a sophisticated program synthesizer at it's core. 
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    It takes a program specification (`Reviewer`) and a set of I/O pairs (`io_pairs`), and returns a tuned program (prompt) that satisfies the spec.
</span>

__Why not guide DSPy with assertions too?__

</section>

<section markdown=1>

## Introducing DSPy Assertions

We introduce a new weapon to DSPy: __LM Assertions__.
As simple as one-liners, they are assertion style constraints on LM outputs.
We distinguish two types of constraints: __Assert__ (hard) and __Suggest__ (soft):
```python
dspy.Assert(constraint: bool, message: str, backtrack: Optional[Module])
dspy.Suggest(constraint: bool, message: str, backtrack: Optional[Module])
```

Unlike regular assertions, LM assertions are more than just monitors.
If the constraint is violated, the execution is paused, and the LM program
attempts to recover from the violation by backtracking to the failing module.
It uses introspective information to self-correct and continue execution.
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/> 
<span class="sidenote">
    Read more about how this works in our [paper](https://github.com/stanfordnlp/dspy/blob/main/DSPy_Assert.pdf).
    This [tweet](https://twitter.com/lateinteraction/status/1735326551393161563) is also a great start.
</span>


#### LM Assertions for a Good Reviewer 🤩

Here's how we can use a few LM assertions to build a good reviewer:
```python
class Reviewer(dspy.Module):
  def __init__(self):
    self.gen_review = dspy.ChainOfThought("pull_request -> review, status")

  def forward(self, pr):
    result = self.gen_review(pull_request=pr)

    # Assert that the review is concise.
    dspy.Assert(len(result.review) < 2000, 
        "review must be concise")

    # Suggest that the review be constructive.
    dspy.Suggest(result.review.startswith("lgtm"), 
        "review must be constructive")

    return result
```

That's it! We can now use DSPy as before to compile a reviewer that satisfies these assertions and suggestions.
Our evaluations show that resulting programs are not just more robust but also more performant.

## Conclusion

DSPy assertions are a powerful tool for guiding LMs toward desired outputs.
There are natural connections between traditional program synthesis and self-refining LM programs with assertions.
We are excited to explore these connections further and build a next generation programming paradigm.

Read more in our [paper](https://github.com/stanfordnlp/dspy/blob/main/DSPy_Assert.pdf) and checkout our [Github](https://github.com/stanfordnlp/dspy/blob/main/dspy/primitives/assertions.py).

</section>