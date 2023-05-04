import coverage

from sample.Quadratic import *


# class TestCar(unittest.TestCase):
def test():

    cov = coverage.Coverage(branch=True)
    cov.start()

    # is_prime(4)
    quadratic(-70, -640, 670, 160, -704)
    # quadratic(-56, 182,861,800,576)
    # quadratic(-296,-257,-894,-879,-238)

    cov.stop()
    data = cov.get_data()

    print(data.measured_files())
    print(data.lines('/Users/hallimede/Downloads/DataScience-T4/Quadratic.py'))
    print(data.arcs('/Users/hallimede/Downloads/DataScience-T4/Quadratic.py'))


test()
