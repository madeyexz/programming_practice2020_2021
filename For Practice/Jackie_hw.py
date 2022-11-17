import datetime
import xpinyin

name = input('请先输入你的姓名: \n')

print(name + '您好！欢迎来到汉语拼音测试小游戏')
print('在游戏中，你需要回答共三道题，输入屏幕显示单词的语文拼音，系统将会记录你的游戏用时')
start = input('请按Y开始游戏:')

p = xpinyin.Pinyin()
print(p.get_pinyin(u'北京',' ',tone_marks='numbers'))