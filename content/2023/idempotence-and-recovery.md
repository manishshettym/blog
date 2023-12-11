Title: Idempotence and Recovery
Date: 2023-10-30 13:09
Category: Research
Tags: PL, Program Analysis, Static Analysis, Program Recovery, Idempotence
Description: Thoughts on finding idempotent program regions for safer recovery.
Status: Published

<section markdown="1">

Recovery capability is an important aspect of modern systems.
In most cases, recovery is used to repair the state of the program in the rare event that an execution
failure occurs.

Checkpoints provide a simple way to implement recovery.
However, they have several challenges:

1. Checkpointing entire program state is expensive.
2. They have limited application visibility and often end up being overly aggresive in saving more state than necessary.

To address these challenges, we could study the core property that 
enables simple recovery via re-execution: **idempotence**.<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
  There are approaches like _transactional semantics_ that can be used to implement efficient recovery.
  However, they require the programming language to support a specific programming model.
</span>

<blockquote markdown="1">
Idempotence is the property of a program that re-execution is free of side-effects.
</blockquote>

In contrast, to explicit checkpointing, idempotence allows the architecture state
at the beginning of a code region to be used as an implicit checkpoint (that is never saved).
On execution failure, idempotence allows repairing the state via a simple re-execution.

The definition of idempotence looks simple, but is not easy to apply in practice.
Particularly challenging is the fact that most real-world programs are not _completely_ idempotent;
they have some side-effects. Let's define side-effects more formally.

</section>

<section markdown="1">
## Side-effects

A side-effect is a change in the state of the program that is not visible to the caller.
For instance, consider the following code snippet:

```python
def foo(x, y):
    return x + y
```

The function `foo` has no side-effects, since it manipulates only the arguments passed to it. In contrast, consider the following code snippet:

```python
total = 0

def bar(x, y):
    global total
    total += x + y
    return total
```

In this version of the function `bar` we have added a global variable `total` outside of the function that is modified. This creates a side effect, since the function now affects something outside of its immeditate scope.

Real-world programs look more like `bar`. They have side-effects that are not visible to the caller. Does this mean that we cannot use idempotence to implement recovery in real-world programs? Not necessarily.

</section>

<!-- https://research.cs.wisc.edu/vertical/papers/2012/pldi12-idem.pdf -->

<section markdown=1>
## Idempotence modulo side-effects

To make idempotence practical for recovery, we can weaken it in the following ways to be applicable in programs with side-effects:

1. allow idempotent side-effects.
2. allow partial idempotence.

__1. Idempotent Side-Effects__

Note, that idempotence is a property of a program's **re-execution**. This means that we can use idempotence, if we can ensure that the re-execution of a program is side-effect free. More generally, we can weaken this definition to state the following:

<blockquote markdown="1">
If the re-execution of a program has the _same_ side-effects as the original execution then the program is idempotent.
</blockquote>

That is to say, if the side-effects of a program are idempotent, then the program is idempotent. For instance, consider the following code snippet:

```python
x = 0

def setx(n):
    global x
    x = 3
```

`setx` has a side-effect because it modifies a global variable `x`. However, it is idempotent because multiple executions has the same effect on the system state as the first application.


__2. Partial Idempotence__

The second way to weaken idempotence is to allow partial idempotence. That is to say, if we are looking to use idempotence for recovery, we can allow regions of the program to be idempotent. For instance, consider the following code snippet:

```python
b = []

def list_push(a, n):
    o = len(a) == 10
    if o: a = b
    a.append(n)
```

The semantics of the function clearly preclude idempotence: even if there is no overflow, re-executing the function will put the element to the end of an _already modified_ list (after the element that was pushed during the original execution).

However, there are regions of the program that are idempotent. For instance, we could split the function into 3 regions as in the control flow graph below:

<pre class="mermaid">
flowchart TD
    a["`o = len(a) == 10 
    if o: a = b`"] --> b["`a = b`"]
    a["`o = len(a) == 10 
    if o: a = b`"] --> c["`a.append(n)`"]
    b["`a = b`"] --> c["`a.append(n)`"]
</pre>

</section>

<section markdown="1">
## Idempotent Code Regions

We can define idempotent code regions as follows:

<blockquote markdown="1">
A region of code (assume linear instruction sequence for now) is idempotent if
the effect of executing the region multiple times is identical to executing
it once.
</blockquote>

An intuitive way to think about this is ***a region that does not overwrite its inputs***.
A region that overwrites its inputs will read the overwritten values on re-execution, changing its behavior.
But what are the inputs of a region?

<subsection markdown="1">
### Region Inputs and Dependencies

Region Inputs are variables that are _LIVE-IN_ to the region; i.e., live at the entry of the region.
Such a variable has a definition that reaches the region's entry and has some use within the region.

By definition of liveness, region inputs have a **RAW**<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    Read-After-Write (RAW) dependency is between a definition and following use of a variable.
    A.K.A _flow dependency_.
</span>
dependency that spans the region's entry.
However, because the definition the variable must be defined before entry, the definition is not inside the region,
and hence no definition precedes the first use of the variable.

<pre class="mermaid">
classDiagram
    Observation : A region input has no RAW dependency\n before the first use of that variable in the region\n*
</pre>

Since region inputs are live at the entry of a region, and have no RAW dependency before the first use,
any overwriting of the variable will have to occur after the first use of the variable.

In other words, an overwriting of region inputs has a **WAR**<label for="sn-demo" class="margin-toggle sidenote-number"></label>
<input type="checkbox" id="sn-demo" class="margin-toggle"/>
<span class="sidenote">
    Write-After-Read (WAR) dependency is between a use and a following (re-)definition of a variable.
    A.K.A _anti-dependency_.
</span>
dependency after the absence of a RAW dependency.

<pre class="mermaid">
classDiagram
    Observation : Overwriting a region input has a WAR dependency\n after the absence of a RAW dependency\n*
</pre>

</subsection>


The table below summarizes the relationship between dependencies and idempotence.

<style>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  text-align: center;
  border: 1px solid black;
  padding: 8px;
}
</style>

<table>
    <thead>
        <tr>
            <th>Dependency</th>
            <th>RAW</th>
            <th>RAW-&gt;WAR</th>
            <th>WAR</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Example</td>
            <td><code>x = 1<br>y = x</code></td>
            <td><code>x = 1<br>y = x<br>x = 2</code></td>
            <td><code>y = x<br>x = 2</code></td>
        </tr>
        <tr>
            <td>Idempotent?</td>
            <td>Yes</td>
            <td>Yes</td>
            <td>No</td>
        </tr>
    </tbody>
</table>


From the above, we can see that one can identify a idempotent code regions by looking for regions that have no WAR dependencies after the absence of a RAW dependency.

</section>

<section markdown="1">

## Conclusion

Idempotence is a powerful property that can be used to implement recovery.
However, it is not easy to apply in practice due to the presence of side-effects in real-world programs.
In this post, we have explored the definition of idempotence and how it can be applied to real-world programs. Particularly, we have seen that idempotence can be applied to regions of code that do not overwrite their inputs. We have also explored a simple way to identify such regions but leave implementing it as a static analysis for a future post.

</section>