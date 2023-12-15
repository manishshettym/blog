Title: DSPy Assertions: A PR Review's POV
Date: 2023-12-15 6:31
Category: Research
Tags: DSPy, LLM, Assertions, Program Recovery, Program Synthesis, PL
Description: Deep connections between traditional program synthesis and self-refining LM programs with assertions.
Status: Published

<section markdown="1">

Prompting emerged as a way to "interact" with LMs due to the naturalness of language.
We soon realized one needs to "engineer" their prompts to get desired outputs from these stochastic machines. _While interactions are natural and imprecise, engineering is anything but._

Mixing the medium for interaction and engineering results in hand-crafted `prompt templates`—an error-prone practice, often verbose, and doesn’t always generalize.

That leads us to the question: **How can we program LMs without prompting?**


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

This program reviews a GitHub pull request:

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
result = reviewer(pr="def add(a, b): return a - b")
print(result.review, result.status)

# review: ... could be improved by renaming 
# the function and adding proper error handling.
# status: Changes requested
```

DSPy also automatically compiles quality few-shot prompts for your program, so you don't have to! You can use it to build a more robust reviewer in a few lines and some I/O pairs.
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    Imagine collecting a few hundred I/O pairs from GitHub PRs and compiling a reviewer that is robust to unseen PRs. 🤩 
    </br></br>
    In the code, `is_valid` is the optimizer metric and could be a fuzzy string match or an LLM call that checks the review's validity.
</span>
```python
teleprompter = BootstrapFewShot(metric=is_valid)
reviewer = teleprompter.compile(Reviewer(), trainset=io_pairs)
```
</section>

<section markdown="1">

## Reflection: Is this a good reviewer? 🤔

<img src="./images/lgtm.jpeg" alt="drawing" width="250" style="float: right; border: dashed;"/>
It is relatively easy to write a valid review for a PR. 

But, a good reviewer writes _concise_, _constructive_, and _informative_ reviews. The question is, __how do we capture and ensure these properties in a program?__

</section>


<section markdown="1">

## "Sketching" the Solution (pun intended)

In traditional program synthesis, particularly in sketching [[Solar-Lezama, 2008]](https://people.csail.mit.edu/asolar/papers/thesis.pdf), developers provide a high-level outline of a program— a __sketch__—along with a set of __assertions__ that specify the desired behavior. The synthesizer then fills in the details, turning the sketch into a fully-fledged program that adheres to the assertions.

<blockquote markdown="1">
Assertions in a sketch enable you to express intuitive insights 
without overthinking the implementation details.
</blockquote>

💡 Wait? By now, we know that DSPy is a sophisticated program synthesizer at its core. 
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    It takes a program specification (`Reviewer`) and a set of I/O pairs (`io_pairs`) and returns a tuned program (prompt) that satisfies the spec.
</span>

__Why not guide DSPy with assertions?__

</section>

<section markdown=1>

## Introducing DSPy Assertions

We introduce to DSPy: __LM Assertions__.
As simple as one-liners, they are assertion style constraints on LM outputs.
We distinguish two types of constraints: __Assert__ (hard) and __Suggest__ (soft):
```python
dspy.Assert(constraint: bool, message: str)
dspy.Suggest(constraint: bool, message: str)
```

Unlike regular assertions, LM assertions are more than just monitors.
On violating the constraint, the execution pauses, and the LM program
attempts to recover from the violation by backtracking to the failing module.
During recovery, the construct uses reflective information to self-correct and continue execution. `Asserts` fail the program if irrecoverable, while `Suggests` continue execution.
<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/> 
<span class="sidenote">
    More about how this works in our [paper](https://github.com/stanfordnlp/dspy/blob/main/DSPy_Assert.pdf).
    This [tweet](https://twitter.com/lateinteraction/status/1735326551393161563) is also a great start.
</span>

Here's how we can use a few LM assertions to build our "good" reviewer:
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
    dspy.Suggest(not result.review.startswith("lgtm"), 
        "review must be constructive")

    return result
```

That's it! We can now use DSPy to compile a reviewer that satisfies these assertions and suggestions. Our paper evaluates these new constructs and finds that resulting programs are more robust and performant!

## Conclusion

DSPy assertions are a powerful tool for guiding LMs toward desired outputs.
There are natural connections between traditional program synthesis and self-refining LM programs with assertions.
We are excited to explore these connections further and build a next-generation programming paradigm.

Read more in our [paper](https://github.com/stanfordnlp/dspy/blob/main/DSPy_Assert.pdf) and checkout our [Github](https://github.com/stanfordnlp/dspy/blob/main/dspy/primitives/assertions.py).

</section>