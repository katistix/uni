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
    
    def multiply(self, other):
        # (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
        real_part = self.real * other.real - self.imaginary * other.imaginary
        imaginary_part = self.real * other.imaginary + self.imaginary * other.real
        return ComplexNumber(real_part, imaginary_part)
    
    def equals(self, other):
        return self.real == other.real and self.imaginary == other.imaginary
    


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

    # Multiplication tests
    n5 = ComplexNumber(2, 1)
    n6 = ComplexNumber(3, 4)
    product = n5.multiply(n6)  # (2+i)*(3+4i) = 6+8i+3i+4i² = 6+11i-4 = 2+11i
    assert(product.real == 2)
    assert(product.imaginary == 11)
    assert(product.get_string() == "2+11i")

    n7 = ComplexNumber(1, 2)
    n8 = ComplexNumber(2, -1)
    product2 = n7.multiply(n8)  # (1+2i)*(2-i) = 2-i+4i-2i² = 2+3i+2 = 4+3i
    assert(product2.real == 4)
    assert(product2.imaginary == 3)
    assert(product2.get_string() == "4+3i")

    # Equality tests
    n9 = ComplexNumber(3, 4)
    n10 = ComplexNumber(3, 4)
    n11 = ComplexNumber(3, 5)
    assert(n9.equals(n10) == True)
    assert(n9.equals(n11) == False)
    assert(n10.equals(n11) == False)
