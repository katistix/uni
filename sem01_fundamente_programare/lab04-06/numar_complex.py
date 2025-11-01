class ComplexNumber:
    def __init__(self, real: int, imaginary: int):
        self._real = real
        self._imaginary = imaginary

    @property
    def real(self):
        return self._real
    
    @real.setter
    def real(self, value):
        self._real = value

    # def get_real(self):
    #     return self.real


    @property
    def imaginary(self):
        return self._imaginary
    
    @imaginary.setter
    def imaginary(self, value):
        self._imaginary = value
    
    # def get_imaginary(self):
    #     return self.imaginary
    
    def get_string(self):
        if(self.imaginary<0):
            return f"{self.real}{self.imaginary}i"

        return f"{self.real}+{self.imaginary}i"
    
    def get_module(self):
        return (self.real**2 + self.imaginary**2)**0.5
    
    def add(self, other):
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)
    


def test_module():
    # Getter tests
    n_complex = ComplexNumber(5,3)
    assert(n_complex.real==5)
    assert(n_complex.imaginary==3)
    
    # Stringify tests
    n_complex = ComplexNumber(5,3)
    assert(n_complex.get_string()=="5+3i")

    n_complex = ComplexNumber(-5,3)
    assert(n_complex.get_string()=="-5+3i")

    n_complex = ComplexNumber(5,-3)
    assert(n_complex.get_string()=="5-3i")

    n_complex = ComplexNumber(-5,-3)
    assert(n_complex.get_string()=="-5-3i")

    # Module tests
    n_complex = ComplexNumber(3,4)
    assert(abs(n_complex.get_module() - 5.0) < 0.001)

    n_complex = ComplexNumber(6,8)
    assert(abs(n_complex.get_module() - 10.0) < 0.001)

    n_complex = ComplexNumber(0,0)
    assert(abs(n_complex.get_module() - 0.0) < 0.001)

    # Addition tests
    n1 = ComplexNumber(3, 4)
    n2 = ComplexNumber(5, 2)
    result = n1.add(n2)
    assert(result.real == 8)
    assert(result.imaginary == 6)
    assert(result.get_string() == "8+6i")

    n3 = ComplexNumber(-2, 3)
    n4 = ComplexNumber(1, -5)
    result2 = n3.add(n4)
    assert(result2.real == -1)
    assert(result2.imaginary == -2)
    assert(result2.get_string() == "-1-2i")
