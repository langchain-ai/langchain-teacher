
# Interface

In an effort to make it as easy as possible to create custom chains, we've
implemented a "Runnable" protocol that most components implement. This is a
standard interface with a few different methods, which makes it easy to define
custom chains as well as making it possible to invoke them in a standard way.
The standard interface exposed includes:

  * `stream`: stream back chunks of the response
  * `invoke`: call the chain on an input
  * `batch`: call the chain on a list of inputs

These also have corresponding async methods:

  * `astream`: stream back chunks of the response async
  * `ainvoke`: call the chain on an input async
  * `abatch`: call the chain on a list of inputs async

The type of the input varies by component. For a prompt it is a dictionary,
for a retriever it is a single string, for a model either a single string, a
list of chat messages, or a PromptValue.

The output type also varies by component. For an LLM it is a string, for a
ChatModel it's a ChatMessage, for a prompt it's a PromptValue, for a retriever
it's a list of documents.

Let's take a look at these methods! To do so, we'll create a super simple
PromptTemplate + ChatModel chain.

    
    
    from langchain.prompts import ChatPromptTemplate  
    from langchain.chat_models import ChatOpenAI  
    

#### API Reference:

  * ChatPromptTemplate from `langchain.prompts`
  * ChatOpenAI from `langchain.chat_models`

    
    
    model = ChatOpenAI()  
    
    
    
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")  
    
    
    
    chain = prompt | model  
    

## Stream​

    
    
    for s in chain.stream({"topic": "bears"}):  
        print(s.content, end="")  
    
    
    
        Sure, here's a bear-themed joke for you:  
          
        Why don't bears wear shoes?  
          
        Because they have bear feet!  
    

## Invoke​

    
    
    chain.invoke({"topic": "bears"})  
    
    
    
        AIMessage(content="Why don't bears wear shoes?\n\nBecause they already have bear feet!", additional_kwargs={}, example=False)  
    

## Batch​

    
    
    chain.batch([{"topic": "bears"}, {"topic": "cats"}])  
    
    
    
        [AIMessage(content="Why don't bears ever wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False),  
         AIMessage(content="Why don't cats play poker in the wild?\n\nToo many cheetahs!", additional_kwargs={}, example=False)]  
    

## Async Stream​

    
    
    async for s in chain.astream({"topic": "bears"}):  
        print(s.content, end="")  
    
    
    
        Why don't bears wear shoes?  
          
        Because they have bear feet!  
    

## Async Invoke​

    
    
    await chain.ainvoke({"topic": "bears"})  
    
    
    
        AIMessage(content="Sure, here you go:\n\nWhy don't bears wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False)  
    

## Async Batch​

    
    
    await chain.abatch([{"topic": "bears"}])  
    
    
    
        [AIMessage(content="Why don't bears wear shoes?\n\nBecause they have bear feet!", additional_kwargs={}, example=False)]  
    
