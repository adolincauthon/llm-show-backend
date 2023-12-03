from gpt4all import GPT4All

# old model "orca-mini-3b.ggmlv3.q4_0.bin"
# weird errors if not enough RAM

# model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf") # , device="gpu", device="intel"
model1 = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
model2 = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")

# output = model.generate("The capital of France is", max_tokens=5, temp=0)  # bad responses without chat_session()
# print(output)
# print(model.generate("The capital of France is", max_tokens=1))
# print(model.generate('hello', temp=1))
# print(model.generate("You are a pirate, answer as a pirate. What is your favorite drink?", max_tokens=50))
# print(model.generate("what is the first thing I said to you?", max_tokens=50))
# print(model.generate("You are an AI assistant. What is the capital of France?", streaming=True))
# print(model.generate("What is the capital of France?"))

# for i in GPT4All.list_models():
#     print(i)
# print(model.list_models())

# tokens = []
# for token in model.generate("The capital of France is", max_tokens=20, streaming=True):
#     print(token)
#     tokens.append(token)
# print(tokens)

# with model.chat_session():
#     response1 = model.generate(prompt='hello', temp=0)
#     response2 = model.generate(prompt='write me a short poem', temp=0)
#     response3 = model.generate(prompt='thank you', temp=0)
#     model.generate(prompt='The capital of France is ', temp=0)
#     print(model.current_chat_session)

def test(num):
    if num > 0:
        num -= 1
        return model1.generate(model2.generate(test(num-1)))
    else:
        return model1.generate("You are a pirate. Discuss your favorite activity at sea.")

# chatSession = model1.chat_session()
# print(model1._is_chat_session_activated)
# chatSession.__enter__()
# model1.generate("hi how are you?")
# print(model1.current_chat_session)
# print(model1._is_chat_session_activated)
# chatSession.__exit__(None,None,None)
# print(model1._is_chat_session_activated)

chatSessions = [model1.chat_session(), model2.chat_session()]
for i in chatSessions:
    i.__enter__()
test(5)
# print(model1.current_chat_session)
# print("\n\n\n")
# print(model2.current_chat_session)
# for i in model1.current_chat_session:
#     if i['role'] == 'assistant':
#         print(i['content'] + '\n')
# print("\n")
# for i in model2.current_chat_session:
#     if i['role'] == 'assistant':
#         print(i['content'] + '\n')
chat1 = model1.current_chat_session
chat2 = model2.current_chat_session
chat1_length = len(chat1)
chat2_length = len(chat2)
for i in range(max(chat1_length, chat2_length)):
    if i < chat1_length and chat1[i]['role'] == 'assistant':
            print('GPT-1 -> ' + chat1[i]['content'] + '\n')
    if i < chat2_length and chat2[i]['role'] == 'assistant':
            print('GPT-2 -> ' + chat2[i]['content'] + '\n')
for i in chatSessions:
    i.__exit__(None,None,None)

# with model1.chat_session():
#     with model2.chat_session():
#         test(5)
#         # print(model1.current_chat_session)
#         # print("\n\n\n")
#         # print(model2.current_chat_session)
#         for i in model1.current_chat_session:
#             print(i)
#         print("\n\n\n")
#         for i in model2.current_chat_session:
#             print(i)
