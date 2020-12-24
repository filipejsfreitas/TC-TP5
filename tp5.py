from math import gcd


def convert_to_plaintext(numbers):
    # Dados blocos de texto (na forma de um inteiro 27 * 27 * L1 + 27 * L2 + L3), conveter esses blocos para texto limpo
    plaintext = ''

    for d in numbers:
        a = chr(ord('A') + d // (27 ** 2))
        b = chr(ord('A') + (d % (27 ** 2)) // 27)
        c = chr(ord('A') + (d % (27 ** 2)) % 27)

        block = a + b + c
        # O caracter espaço é representado por 0x20, enquanto que a primeira letra do alfabeto é representada por 0x41.
        # Isto significa que o número 26 vai ser descodificado no caracter 0x5B, que é o caracter [, e portanto, vamos fazer uma simples
        # substituição para substituir o [ por um espaço, de modo a que o resultado final fique correto
        block = block.replace('[', ' ')

        plaintext += block
    
    return plaintext


def rsa(numbers, n, e):
    # Aplicação do RSA:
    # Exponenciação modular utilizando as funções nativas do Python
    result = []

    for x in numbers:
        result.append(pow(x, e, n))
    
    return result


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    
    g, y, x = egcd(b % a, a)

    return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)

    if g != 1:
        raise Exception('modular inverse does not exist')
    
    # egcd(a, m) returns: gcd(a,b), and also the x, y factors for the diophantine equation ax + my = g
    # That means that x % m is the modular inverse of a mod m
    return x % m


if __name__ == '__main__':
    f = open('ciphertext.txt', 'r', encoding='UTF-8')
    lines = f.readlines()
    # Processamento básico das linhas de entrada:
    # Remover espaços extra, remover strings vazias, etc.
    # No final, converter todas as strings para números
    numbers = [int(x.strip()) for line in lines for x in line.split(',') if len(x.strip()) > 0] 
    f.close()

    # Resultado do pré-processamento
    print(numbers)

    # Parâmetros públicos do RSA
    e = 17
    n = 213271

    # Queremos calcular os fatores p, q de n
    p, q = None, None

    # Calcular o fator p tal que n % p == 0 por força bruta
    # Como n é relativamente pequeno, este processo é rápido o suficiente
    for x in range(2, n):
        if n % x == 0:
            p = x
            break

    # O outro fator, q, é simplesmente n // p
    q = n // p

    # Imprimir p, q, p * q e n
    print(p, q, p * q, n)

    # Calcular phi(n) = (p-1) * (q-1)
    totient_n = (p-1) * (q-1)

    # Imprimir o máximo divisor comum de e e phi(n)
    print(gcd(e, totient_n))

    # Calcular o parâmetro d privado tal que
    # d = e^-1 (mod n)
    d = modinv(e, totient_n)

    # Decifrar o RSA usando o parâmetro d privado
    decrypted_numbers = rsa(numbers, n, d)

    # Converter os blocos de três letras nas suas letras componentes
    print(convert_to_plaintext(decrypted_numbers))
