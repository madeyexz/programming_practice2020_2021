from pythonds.basic.stack import Stack
import re

def infixToProfix(expression):
    # 中缀转前缀
    # 输入：一个表示中缀表达式的字符串，字符串由英文大小写字母、数字以及+-*\()组成，中间不带空格，如"(3+4)*5-6"或者"(a-b/c)*(a/k-l)"。
    # 输出：一个将中缀表达式转化为前缀表达式的字符串，如"-*+3456"或者"*-a/bc-/akl"，注意中间不包含空格
    prec = {}
    prec['*'] = 3
    prec['/'] = 3
    prec['+'] = 2
    prec['-'] = 2
    prec[')'] = 1

    opStack = Stack()
    prefixList = []
    tokenList = [char for char in expression][::-1]

    for token in tokenList:
        # 如果是操作数，直接加入prefixList
        if token in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890':
            prefixList.append(token)
        # 遇到右括号直接压入栈中
        elif token == ')':
            opStack.push(token)
        # 如果遇到一个左括号，那么就将栈元素弹出并加到Temp表达式尾端，但左右括号并不输出
        elif token == '(':
            topToken = opStack.pop()
            while topToken != ')':
                prefixList.append(topToken)
                topToken = opStack.pop()
        # 如果是运算符，则比较优先级
        # 若该运算符优先级大于等于栈顶元素，则将该运算符入栈，
        # 否则栈内元素出栈并加到Temp表达式尾端，直到该运算符大于等于栈顶元素的优先级时，再将该运算符压入栈中
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                prefixList.append(opStack.pop())
            opStack.push(token)
    # 最后，若运算符栈中还有元素，则将元素一次弹出并加到Temp表达式尾端
    while not opStack.isEmpty():
        prefixList.append(opStack.pop())
    # 最后一步是将Temp表达式翻转
    return ''.join(prefixList[::-1])

def isHtmlTagMatch(htmlFile):
    # 扩展括号匹配
    # 输入：html文档名
    # 输出：布尔变量，如果HTML文档的标记匹配，输出True，否则输出False
    s = Stack()
    index = 0
    balanced = True
    with open(htmlFile, encoding='utf8') as f:
        html = f.read()
        tags = re.findall('<([^>]+)>',html)

        while index < len(tags) and balanced == True:
            if '/' not in tags[index]:
                s.push(tags[index])
            else:
                if s.isEmpty() == 1:
                    balanced = False
                    break
                else:
                    if s.peek() in tags[index]:
                        s.pop()
                    else:
                        balanced = False
                        break
            index += 1

        if balanced and s.isEmpty():
            return True
        else:
            return False
        
def main():
    infixexpr = "(3+4)*5-6"
    print(infixToProfix(infixexpr))

    htmlFile = 'example.html'
    print(isHtmlTagMatch(htmlFile))

if __name__ == '__main__':
    main()