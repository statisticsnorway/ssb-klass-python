import os
notebook_path = os.getcwd()
while ".ssb_project_root" not in os.listdir():
    os.chdir("../")
from src.functions.fizzbuzz import fizz, buzz, fizzbuzz


def test_fizz():
    assert fizz(3) == "fizz"
    assert fizz(4) == ""

def test_buzz():
    assert buzz(5) == "buzz"
    assert buzz(6) == ""

def test_fizzbuzz():
    assert fizzbuzz([15]) == ["fizzbuzz"]
    assert fizzbuzz([3]) == ["fizz"]
    assert fizzbuzz([5]) == ["buzz"]
    assert fizzbuzz([2]) == [2]