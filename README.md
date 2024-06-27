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
* Let's extend it to use `langchain` ([answer here](./01-gradio))

## Machine Learning Primer *or* What the heck are 'top_p' and 'temperature'?

* Markov Generators are easy to code and a useful starting point for gaining a basic understanding of what's going on in an LLM model
* Markov Generators build a Markov Model (shocking) from a set of input texts, which is just a mapping of "if you're sitting looking at word A, how likely is it that the next word is word B?"
* Let's build a simple Markov Generator to mess around ([answer here](./02-markov))
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

## Prompt engineering

* As a starting off point, if we only had a text generation LLM and it didn't already support chat. How would we layer in chat?
* We might ask it to "generate a conversation between a user and an AI", then seed it with the user's message, ie:
```
	Here is a conversation between a user and a helpful AI assistant:

	User: Hello, how are you?
	AI: Hi! I'm well. How can I help you?
	User: {message}
	AI:
```
* This is an example of _prompt engineering_. The model doesn't keep any state--it's a static set of trained numbers. But we can "fake" state by passing it everything it needs when we ask it to generate. This is a little like HTTP cookies.
* Since we control all the input to the model, we can augment it with any instructions or information we like.
* The primary limitation is _context_, which is the length of the prompt we're able to pass to the model. For some models this may only be a thousand words or so!

## Other stuff to check out

* Retrieval augmented generation (RAG)
	* Build a context dynamically with the most relevant information
	* [langchain example](https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/)
* Agents
	* As we've seen, LLMs can be pretty good at reasoning... what if we let them decide what to do next? Spawn off other questions? Consolidate information? And only then generate a respone?
	* [langchain exmaple](https://python.langchain.com/v0.1/docs/modules/agents/quick_start/)
* Fine-tuning
	* "Stack" new machine learning examples on top of the existing model. This tweaks the parameters. Good for adding domain information that does not change.
	* [HuggingFace AutoTrain](https://huggingface.co/autotrain)

## Profession responsibility and ethics

* Revolutionary = dangerous
* LLMs can hallucinate and users may give them undue trust because they think of computers as infallible. You have a professional duty to let folks know you're using AI!
* LLMs absorb the biases of the text on which they are trained. When asked to function as recruiters, LLMs are more likely to recommend against hiring candidates who show African American word usage, without ever actually knowing they are Black
