"""package"""


package_var_noshow = 1

package_var: int = 1
"""This is a package variable that was documented"""


@this_decorator(darg, dkwarg=2)
def package_function(arg: int, kwarg: str = "a") -> str:
    """this is a package function"""
    return "yay"


class PackageClass:
    def __init__(self, arg: str, kwarg: int = 1) -> list:
        """Class documentation goes here"""
        pass

    def method(self, rawr):
        """this is a class method"""
        return True
