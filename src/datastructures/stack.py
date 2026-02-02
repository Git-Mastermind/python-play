class Stack():
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)				

    def pop(self):
        return self.items.pop()
    
    def is_empty(self):
        return self.items == []
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        
    def get_stack(self):
        return self.items
    
    def is_match(self, paren1, paren2):
        if paren1 == ")" and paren2 == "(":
            return True
        if paren1 == "]" and paren2 == "[":
            return True
        if paren1 == "}" and paren2 == "{":
            return True
        else:
            return False
    
    def is_parenthesis_balanced(self, paren):
        index = 0
        is_balanced = True
        if len(paren) == 1:
            return False
        while index < len(paren):
            if paren[index] in "([{":
                self.push(paren[index])
            else:
                if self.is_empty():
                    is_balanced = False
                    return is_balanced
                else:
                    if self.is_match(paren[index], self.pop()):
                        is_balanced = True
                    else:
                        is_balanced = False
                        return is_balanced
            index += 1
        if self.is_empty():
            return True
        else:
            return False
    
    def reverse_string(self, string):
        reversed_string = []
        for i in range(len(string)):
            self.push(string[i])
        for i in range(len(string)):
            reversed_string.append(self.pop())
        return "".join(reversed_string)

stacks = Stack()
print(stacks.reverse_string("Hello"))
            
