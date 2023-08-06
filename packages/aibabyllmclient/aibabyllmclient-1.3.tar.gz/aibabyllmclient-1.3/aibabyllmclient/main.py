# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from aibabyllmclient.llmserver_call import call_llmserver


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    call_llmserver("李白是？","10.1.100.95","50007")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
