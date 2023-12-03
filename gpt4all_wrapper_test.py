from typing import Iterable
from gpt4all_wrapper import GPT


def main():
    gpt = GPT()
    test(gpt, 5)
    chat1 = gpt.getChatHistory(0)
    chat2 = gpt.getChatHistory(1)
    chat1_length = len(chat1)
    chat2_length = len(chat2)
    for i in range(max(chat1_length, chat2_length)):
        if i < chat1_length and chat1[i]['role'] == 'assistant':
                print('GPT-1 -> ' + chat1[i]['content'] + '\n')
        if i < chat2_length and chat2[i]['role'] == 'assistant':
                print('GPT-2 -> ' + chat2[i]['content'] + '\n')
    # for i in range(gpt.numModels):
    #     for j in gpt.getChatHistory(i):
    #         if j['role'] == 'assistant':
    #             print(j['content'] + '\n')
    #     print("\n")
    gpt.endAllChatSessions()


def test(gpt: GPT, num: int) -> (str | Iterable[str]):
    if num > 0:
        num -= 1
        return gpt.generateSimple(0, gpt.generateSimple(1, test(gpt, num-1)))
    else:
        return gpt.generateSimple(0,
                    "You are a pirate. Discuss your favorite activity at sea.")


if __name__ == "__main__":
    main()
