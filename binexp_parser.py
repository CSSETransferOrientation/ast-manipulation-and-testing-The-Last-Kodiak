#!/usr/bin/python3
import os
from os.path import join as osjoin
from enum import Enum

NodeType = Enum('BinOpNodeType', ['number', 'cross', 'timex'])

class BinOpAst:
    def __init__(self, prefix_list):
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = None
            self.right = None
        elif self.val == '+':
            self.type = NodeType.cross
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)
        else:
            self.type = NodeType.timex
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        ilvl = '  ' * indent
        left = f'\n  {ilvl}{self.left.__str__(indent + 1)}' if self.left else ''
        right = f'\n  {ilvl}{self.right.__str__(indent + 1)}' if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        return str(self)

    def prefix_str(self):
        if not self.right:
            return self.val
        return f"{self.val} {self.left.prefix_str()} {self.right.prefix_str()}"

    def infix_str(self):
        if self.type == NodeType.number:
            return self.val
        return f"({self.left.infix_str()} {self.val} {self.right.infix_str()})"

    def postfix_str(self):
        if self.type == NodeType.number:
            return self.val
        return f"{self.left.postfix_str()} {self.right.postfix_str()} {self.val}"

    def additive_identity(self):
        if not self.right:
            return self
        if self.type == NodeType.cross:
            if self.right.val == '0':
                return self.left
            if self.left.val == '0':
                return self.right
        self.left = self.left.additive_identity()
        self.right = self.right.additive_identity()
        return self

    def multiplicative_identity(self):
        if not self.right:
            return self
        if self.type == NodeType.timex:
            if self.right.val == '1':
                return self.left
            if self.left.val == '1':
                return self.right
        self.left = self.left.multiplicative_identity()
        self.right = self.right.multiplicative_identity()
        return self

    def mult_by_zero(self):
        if not self.right:
            return self
        if self.type == NodeType.timex:
            if self.right.val == '0' or self.left.val == '0':
                return BinOpAst(['0'])
        self.left = self.left.mult_by_zero()
        self.right = self.right.mult_by_zero()
        return self

def tester():
    testbench = osjoin('testbench')
    for calculon in os.listdir(testbench):
        print(calculon)
        input_dir = osjoin(testbench, calculon, 'inputs')
        output_dir = osjoin(testbench, calculon, 'outputs')
        for quest in os.listdir(input_dir):
            with open(osjoin(input_dir, quest)) as infile:
                question = infile.read()
                expression = question.split()
            with open(osjoin(output_dir, quest)) as outfile:
                expected = outfile.read()
            test = BinOpAst(expression)
            if calculon == 'arith_id':
                test = test.additive_identity()
            elif calculon == 'mult_id':
                test = test.multiplicative_identity()
            elif calculon == 'mult_by_zero':
                test = test.mult_by_zero()
            answer = test.prefix_str()
            if answer == expected:
                print(f'Input: {question}\nExpected: {expected}\nOutput: {answer}\nTest Case Passed\n')
            else:
                print(f'Input: {question}\nExpected: {expected}\nOutput: {answer}\nTest Case Failed\n')

if __name__ == "__main__":
    tester()
