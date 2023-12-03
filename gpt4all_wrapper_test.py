from typing import Iterable
from gpt4all_wrapper import GPT


def main():
    gpt = GPT()
    test(gpt, 5)
    for i in range(gpt.numModels):
        for j in gpt.getChatHistory(i):
            if j['role'] == 'assistant':
                print(j['content'])
        print("\n\n\n")
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
