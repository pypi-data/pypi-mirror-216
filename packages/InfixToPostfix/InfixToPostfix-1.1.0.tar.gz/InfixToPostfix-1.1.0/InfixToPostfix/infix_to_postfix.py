import os.path
import string


class InfixToPostfix:
    CONFI_PATH = os.path.join(os.path.dirname(__file__), "data/conf")

    @staticmethod
    def is_value(value) -> bool:
        for char in value:
            if char not in string.ascii_lowercase:
                break
        else:
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def __init__(self, conf_path=CONFI_PATH):
        with open(conf_path, "r") as f:
            self.grammar_raw = f.read().split("\n")
        self.grammar_fixed = self.fixed()
        self.non_ters = self.non_ters()
        self.ters = self.ters()
        self.ops = self.ops()
        self.first_vts, self.follow_vts = self.first_and_last_vts()
        self.priority_table = self.priority_table()

    def fixed(self):
        """
        将 grammar_raw 转换成程序可以理解的形式
        """
        grammar_fixed = {"S": [f"#{self.grammar_raw[0][0]}#"]}
        for production in self.grammar_raw:
            left, right = production.split("->")
            grammar_fixed[left] = right.split("|")
        return grammar_fixed

    def non_ters(self):
        return list(self.grammar_fixed.keys())

    def ters(self):
        return list({char for candidates in self.grammar_fixed.values() for candidate in candidates for char in candidate if char not in self.non_ters})

    def ops(self):
        return [ter for ter in self.ters if ter != "v"]

    def first_and_last_vts(self):
        """
        生成 first_vts 和 last_vts
        """

        def first_or_last_vt(non_ter, waited, vt_dict, pattern):
            if non_ter not in waited:
                waited.add(non_ter)
                for candidate in self.grammar_fixed[non_ter]:
                    tmp = candidate[0] if pattern == "first" else candidate[-1]
                    if tmp in self.ters:
                        vt_dict[non_ter].add(tmp)
                    elif tmp in self.non_ters:
                        if tmp not in waited:
                            first_or_last_vt(tmp, waited, vt_dict, pattern)
                            vt_dict[non_ter].update(vt_dict[tmp])
                        if (pattern == "first") and (len(candidate) > 1) and (candidate[1] in self.ters):
                            vt_dict[non_ter].add(candidate[1])
                        elif (pattern == "last") and (len(candidate) > 1) and (candidate[-2] in self.ters):
                            vt_dict[non_ter].add(candidate[-2])

        first_vts, last_vts = {non_ter: set() for non_ter in self.non_ters}, {non_ter: set() for non_ter in self.non_ters}
        for non_ter in self.non_ters:
            first_or_last_vt(non_ter, set(), first_vts, "first")
            first_or_last_vt(non_ter, set(), last_vts, "last")
        return first_vts, last_vts

    def priority_table(self):
        """
        生成算符优先级表
        """

        priority_table = {ter: {ter: "N" for ter in self.ters} for ter in self.ters}
        for candidates in self.grammar_fixed.values():
            for candidate in candidates:
                index = 0
                while index < len(candidate):
                    char = candidate[index]
                    if char in self.ters:
                        if index - 1 > -1:
                            tmp = candidate[index - 1]
                            if tmp in self.non_ters:
                                for left in self.follow_vts[tmp]:
                                    priority_table[left][char] = ">"
                        if index + 1 < len(candidate):
                            tmp = candidate[index + 1]
                            if tmp in self.non_ters:
                                for right in self.first_vts[tmp]:
                                    priority_table[char][right] = "<"
                        if index + 2 < len(candidate):
                            tmp = candidate[index + 2]
                            if tmp in self.ters:
                                priority_table[char][tmp] = "="
                    index += 1
        return priority_table

    def analyze(self, expression):
        """
        对预处理后的元素进行规约和翻译
        """

        def split(expression_inner):
            """
            将表达式 expression_inner 分解，方便后续程序识别
            """
            expression_split = []
            index = 0
            while index < len(expression_inner):
                char = expression_inner[index]
                if char in self.ops:
                    expression_split.append((char, char))
                    index += 1
                else:
                    end = index
                    while (end < len(expression_inner)) and (expression_inner[end] in (string.ascii_lowercase + string.digits + ".")):
                        end += 1
                    value = expression_inner[index:end]
                    if InfixToPostfix.is_value(value):
                        expression_split.append(("v", value))
                    else:
                        raise ValueError(f"{value} 不是一个正常的值")
                    index = end
            return expression_split

        actions, stack, words, stack_states = ["init stack"], [("#", ["#"])], split(expression) + [("#", "#")], ["#"]
        words_states = ["".join([word[1] for word in words])]

        i = 0
        while i < len(words):
            word = words[i]
            j = len(stack) - 1 if stack[len(stack) - 1][0] in self.ters else len(stack) - 2
            while True:
                priority = self.priority_table[stack[j][0]][word[0]]
                if (priority == "<") or (priority == "="):
                    break
                elif priority == ">":
                    while True:
                        right = stack[j][0]
                        j = j - 1 if stack[j - 1][0] in self.ters else j - 2
                        left = stack[j][0]
                        if self.priority_table[left][right] == "<":
                            break
                    # 规约并翻译
                    tmp = stack[j + 1:]
                    if (tmp[0][0] == "Z") and (tmp[1][0] in self.ops) and (tmp[2][0] == "Z"):
                        a = ("Z", [*tmp[0][1], *tmp[2][1], tmp[1][1]])
                    elif (tmp[0][0] == "(") and (tmp[1][0] == "Z") and (tmp[2][0] == ")"):
                        a = ("Z", tmp[1][1])
                    elif tmp[0][0] == "v":
                        a = ("Z", [tmp[0][1]])
                    else:
                        actions.append("无法规约")
                        return words, actions, stack_states, None
                    stack = stack[:j + 1] + [a]
                    actions.append(f"{stack[j][0]} > {word[0]}, {''.join([ele[0] for ele in tmp])} -> Z, Z.code = {' '.join(a[1])}")
                    stack_states.append(f"{''.join([ele[0] for ele in stack])}")
                    words_states.append("".join([word[1] for word in words[i:]]))
            priority = self.priority_table[stack[j][0]][word[0]]
            if (priority == "<") or (priority == "="):
                stack.append(word)
                actions.append(f"{stack[j][0]} <= {word[0]}, stack append {word[1]}")
                stack_states.append(f"{''.join([ele[0] for ele in stack])}")
                words_states.append("".join([word[1] for word in words[i + 1:]]))
            i += 1
        return stack[1][1], words[:-1], actions, stack_states, words_states
