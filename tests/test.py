import sys

sys.path.insert(1, './../')

from Packs.main import Main


def test_install():
    assert list(Main(['python', 'main', 'pillow', 'six']).install()) == ['ok', 'ok'], "Should be ['ok', 'ok']"
    assert list(Main(['python', 'main', 'asdasdasda', 'six']).install()) == ['error', 'ok'], "Should be ['error', 'ok']"


def test_remove():
    assert list(Main(['python', 'main', 'asdasdasda', 'six', '-y']).remove()) == ['error', 'ok'], "Should be ['error', 'ok']"
    

if __name__ == '__main__':
    test_install()
    print('Everything passed')