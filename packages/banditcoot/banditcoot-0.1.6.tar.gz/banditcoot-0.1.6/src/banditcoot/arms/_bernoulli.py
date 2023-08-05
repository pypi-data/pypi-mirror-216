"""This module does blah blah."""

import random

class BernoulliArm():
    """This class does blah blah."""
    def __init__(self, p):
        self.p = p

    def draw(self):
        """This function does blah blah."""
        if random.random() > self.p:
            return 0.0
        return 1.0
