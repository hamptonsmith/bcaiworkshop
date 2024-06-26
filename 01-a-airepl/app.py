import os

def respond(
    message,
    history: list[tuple[str, str]],
    model,
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    yield 'Hi, '
    yield 'Hi, how'
    yield 'Hi, how are'
    yield 'Hi, how are you?'

def printIter(i):
    lastOutput = ''

    for chunk in i:
        print(chunk[len(lastOutput):], end='', flush=True)
        lastOutput = chunk

    print()

while True:
    print()
    text = input('? ')

    if text == '': break

    print()

    printIter(respond(text, [], 'HuggingFaceH4/zephyr-7b-beta', 
    		'You are a friendly AI assistant.', 2000, 0.7, 0.95))

    print()