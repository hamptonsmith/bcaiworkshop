# Build Carolina LLM Workshop

## Lecturer
Dr. Hampton Smith

## Goals
* Learn how to stand up and integrate with various LLM models
* Acquire a toolkit of libraries and services for integrating with LLMs
* Gain confidence with general AI terminology and techniques
* Explore the primary LLM programming model: prompt engineering
* Establish starting points for a variety of future exploration, including training, fine-tuning, and retrieval-augmented generation

## Random resources you might want to check out later
* Three Blue One Brown's [Visualizing Attention](https://www.youtube.com/watch?v=eMlx5fFNoYc)
* The famous [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) paper

## Standing up a simple LLM model

* [huggingface.co](http://huggingface.co) is a machine learning platform
* Good place to find and experiment with LLM models
* At present you can quickly deploy [Gradio](https://www.gradio.app/guides/quickstart) on Hugging Face's "Spaces" platform (for free!)
* Gradio simplifies getting a web interface in front of AI models
* Hugging Face's [Inference API](https://huggingface.co/docs/api-inference/index) platform lets you chat with any AI in their library subject to a couple constraints:
	* Constraints
		* There is a model size limit (currently 10GB, this mostly limits you to toy models)
		* For plug-and-play "chat" functionality, there needs to be a `chat_template` field in their `tokenizer_config.json` (but with a little more work we can get around this by rolling our own template)
	* A good litmus is if the model page has the live chat widget enabled and it's in "chat" mode, not "text generation" mode

## Using `langchain` for a consistent interface

* [langchain](https://python.langchain.com/v0.2/docs/introduction/) is an open source Python library for AI interoperability (and other stuff too)
* Now we can code Gradio to interact with `langchain`, then plug in different backend AIs (Hugging Face Inference, OpenAI, Claude, whatever)
* Let's use [./01-a-airepl](this basic REPL) to avoid having to download Gradio locally, then try to extend it to use `langchain` ([./01-b-airepl](answer here))

## Machine Learning Primer *or* What the heck are 'top_p' and 'temperature'?

* Markov Generators are easy to code and a useful starting point for gaining a basic understanding of what's going on in an LLM model
* Markov Generators build a Markov Model (shocking) from a set of input texts, which is just a mapping of "if you're sitting looking at word A, how likely is it that the next word is word B?"
* Let's build a simple Markov Generator to mess around ([./02-markov](answer here))
* So that's fun. But so what? The reality is this simple machine learning exercise mirrors what's happening in modern LLMs. In a Markov model we build a DAG, while in an LLM we build something signficantly more complicated, but the inputs: the order and frequencies of words, and the outputs: a list of probabilities of "what word is likely to come next" are exactly the same. Understanding this gives us a good framework to explore vocabulary.
	* As a side note, if you're interested in the "significantly more complicated" part, Three Blue One Brown has [an excellent visualization](https://www.youtube.com/watch?v=eMlx5fFNoYc) of it to get you started thinking the right way
	* After which you might try to tackle the [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) paper, or find a softer introduction to the math elsewhere
* So now we can understand `top_p`. Some transitions of words are probably pretty rare and represent either a mistake or a "weird" usage. If we set `top_p=.95` we're saying, "Only worry about those words that form 95% of all of the probability. Get rid of the rest." This eliminates truly strange transitions.
	* Many libraries also have `top_k`, which means "Only keep the most-likely *k* words." But ChatGPT has started to discourage its use and other models seem to be following suit.
* ...and we can understand `temperature`. If one usage is _really_ common ("Once upon a *time*...") we might not want to _always_ pick that one, so we can rescale weights so that even rarer transitions have a chance to get picked up. Temperature makes the word choice more exciting.
* ...and we can understand why LLMs *hallucinate*. They're just guessing a next word that "sounds right". Often a good way to "sound right" is to say true things, but absent that the next best thing is to "make up authoritative-sounding nonsense."
* ...and we've also got a pretty good starting point for the rest of the vocab:

## Vocabulary

* **Parameter** - in the Markov model, the weights on the probabilities from word to word are the parameters. We used (simple) machine learning to train these parameters rather than provideing them by hand.
* **Model** - the set of all the parameters is the model. Importantly the model is *static* so we can invest a lot of computational power up front to discover the "rules" of the language and then reuse all that work
* **Token** - in the Markov model the words are the tokens, and splitting our texts into words is the process of tokenization. In reality, tokens are often smaller than words--in "playing" there is value in treating "play" and "ing" as separate tokens
* **Attention** - the fundamental weakness of a Markov Generator is that it's only paying *attention* to the most recent token. Ideally we'd somehow figure out which previous words in context are the most important to give our attention and then combine their weights somehow

And some bonus vocab:

* **AI** - as with "crypto" before it, we have to distinguish between what it *used* to mean and what it means "in the context of the most recent boom". As a "Hampton-ism", I call the old stuff "classical AI" (teaching computers to reason with a variety of techniques). The new stuff is new enough that I don't think we've settled on a vocaulary--many folks seem to be calling it "transformer-based AI", but I hate that. So as a Hampton-ism, I'm using "attention-based AI." "Attention" is the key innovation here.
* **LLM** - large language model. The "model" here is the pre-built set of weights like we built for the Markov Model, but representing an attention-based neural network rather than a simple DAG. The "large language" part indicates that we're analyzing truly enormous corpuses of written language (in many examples, a large portion of the Internet) and in so doing gaining deep insights about linguistic syntax, semantics, and ontologies that even the human writers may not be aware of.
* **Transformer** - in the context of a neural network, an architecture introduced in the *Attention Is All You Need* paper that decides which words in an input are most strongly related and calls *attention* to those words by "mixing" (i.e., transforming) their probability weights. Transformers are just a way of efficiently implementing attention.

## The key innovation *or* What changed?

So why are we in an AI boom? What changed?

Two things:

1) The transformer architecture was an innovation that let us more efficiently parrallelize the attention technique onto GPUs
2) This revealed how useful the technique was and made it worth investing the necessary upfront costs--I've heard one estimate of $1.5M just of computing time?--just to build the necessary upfront model off of a huge language corpus

Once that model existed, because it's static and reusable, now we all get to use it. And the clear possibilities of this tech means others have invested in building their own models, and researching how to bring the cost of the initial training down.