import array
import string
from abc import ABC, abstractmethod

import httpx


class CryptoAlgorithm(ABC):
    @abstractmethod
    def encrypt(self, text):
        ...

    @abstractmethod
    def decrypt(self, text):
        ...


class ShiftEncryption(CryptoAlgorithm):
    """
    This class provides shift encryption and decryption functionality using the shift cipher algorithm.
    """

    def __init__(self, shift: int = 3):
        self.shift = shift
        self.alphabet_size = 26

    def apply_shift_cipher(self, text: str, method: str) -> str:
        """
        Applies the shift cipher algorithm to the given text based on the specified method.
        :param text: The text to be encrypted or decrypted.
        :param method: The method to be applied, either "encrypt" or "decrypt".
        :return: The encrypted or decrypted text.

        To run the doctests: pytest --doctest-modules -vvs <filename>.py

        >>> shift_3_encryption = ShiftEncryption()
        >>> shift_3_encryption.apply_shift_cipher("Hello World!", "encrypt")
        'Khoor Zruog!'
        >>> shift_3_encryption.apply_shift_cipher("Khoor Zruog!", "decrypt")
        'Hello World!'
        >>> shift_3_encryption.apply_shift_cipher("ZZZZZZ", "encrypt")
        'CCCCCC'
        >>> shift_3_encryption.apply_shift_cipher("CCCCCC", "decrypt")
        'ZZZZZZ'
        >>> shift_4_encryption = ShiftEncryption(shift=4)
        >>> shift_4_encryption.apply_shift_cipher("Hello World!", "encrypt")
        'Lipps Asvph!'
        >>> shift_4_encryption.apply_shift_cipher("Lipps Asvph!", "decrypt")
        'Hello World!'
        >>> shift_4_encryption.apply_shift_cipher("ZZZZZZ", "encrypt")
        'DDDDDD'
        >>> shift_4_encryption.apply_shift_cipher("DDDDDD", "decrypt")
        'ZZZZZZ'
        """
        chars: list = []
        for char in text:
            if char.isalpha():
                base: int = ord("A") if char.isupper() else ord("a")
                if method == "encrypt":
                    char: str = chr((ord(char) - base + self.shift) % self.alphabet_size + base)
                else:
                    char: str = chr((ord(char) - base - self.shift) % self.alphabet_size + base)
            chars.append(char)
        return "".join(chars)

    def encrypt(self, text: str) -> str:
        """
        Encrypts the given text using the shift cipher algorithm.
        :param text: The text to be encrypted.
        :return: The encrypted text.
        """
        return self.apply_shift_cipher(text, method="encrypt")

    def decrypt(self, encrypted_text) -> str:
        """
        Decrypts the given text using the shift cipher algorithm.
        :param encrypted_text: The text to be decrypted.
        :return: The decrypted text.
        """
        return self.apply_shift_cipher(encrypted_text, method="decrypt")


class MatrixEncryption(CryptoAlgorithm):
    # representing the key matrix as a 1D array of bytes,
    byte_key_matrix: bytes = array.array(
        "d",
        [
            8.000,
            4.000,
            4.000,
            8.000,
            7.000,
            8.000,
            7.000,
            1.000,
            9.000,
            4.000,
            1.000,
            1.000,
            1.000,
            6.000,
            3.000,
            0.000,
            9.000,
            6.000,
            0.000,
            0.000,
            5.000,
            4.000,
            2.000,
            3.000,
            1.000,
            4.000,
            7.000,
            8.000,
            2.000,
            6.000,
            0.000,
            5.000,
            0.000,
            7.000,
            2.000,
            4.000,
            4.000,
            9.000,
            4.000,
            0.000,
            1.000,
            1.000,
            3.000,
            1.000,
            2.000,
            7.000,
            0.000,
            7.000,
            9.000,
            5.000,
            9.000,
            7.000,
            8.000,
            3.000,
            2.000,
            6.000,
            5.000,
            5.000,
            6.000,
            1.000,
            6.000,
            8.000,
            4.000,
            6.000,
            5.000,
            1.000,
            7.000,
            1.000,
            1.000,
            0.000,
            2.000,
            9.000,
            8.000,
            6.000,
            0.000,
            9.000,
            5.000,
            5.000,
            6.000,
            3.000,
            3.000,
            9.000,
            8.000,
            4.000,
            0.000,
            4.000,
            5.000,
            0.000,
            1.000,
            0.000,
            9.000,
            6.000,
            6.000,
            7.000,
            0.000,
            7.000,
            7.000,
            1.000,
            8.000,
            3.000,
            1.000,
            0.000,
            2.000,
            1.000,
            0.000,
            1.000,
            3.000,
            3.000,
            7.000,
            5.000,
            5.000,
            3.000,
            6.000,
            1.000,
            4.000,
            3.000,
            9.000,
            5.000,
            1.000,
            2.000,
            9.000,
            7.000,
            5.000,
            4.000,
            2.000,
            5.000,
            0.000,
            0.000,
            9.000,
            3.000,
            7.000,
            5.000,
            0.000,
            4.000,
            4.000,
            2.000,
            5.000,
            9.000,
            3.000,
            1.000,
            6.000,
            6.000,
            7.000,
            4.000,
            3.000,
            2.000,
            3.000,
            4.000,
            4.000,
            1.000,
            5.000,
            1.000,
            1.000,
            0.000,
            6.000,
            5.000,
            1.000,
            2.000,
            8.000,
            3.000,
            6.000,
            6.000,
            0.000,
            7.000,
            2.000,
            7.000,
            1.000,
            0.000,
            2.000,
            6.000,
            4.000,
            2.000,
            2.000,
            9.000,
            4.000,
            0.000,
            9.000,
            7.000,
            7.000,
            3.000,
            1.000,
            5.000,
            1.000,
            0.000,
            9.000,
            5.000,
            4.000,
            9.000,
            3.000,
            6.000,
            6.000,
            0.000,
            6.000,
            4.000,
            9.000,
            3.000,
            9.000,
            7.000,
            8.000,
            8.000,
            3.000,
            8.000,
            2.000,
            1.000,
            5.000,
            9.000,
            5.000,
            2.000,
            4.000,
            2.000,
            1.000,
            7.000,
            0.000,
            2.000,
            7.000,
            9.000,
            2.000,
            8.000,
            5.000,
            7.000,
            6.000,
            7.000,
            1.000,
            9.000,
            4.000,
            2.000,
            4.000,
            2.000,
            9.000,
            4.000,
            6.000,
            2.000,
            2.000,
            6.000,
            3.000,
            0.000,
            6.000,
            7.000,
            3.000,
            2.000,
            5.000,
            9.000,
            1.000,
            4.000,
            2.000,
            3.000,
            1.000,
            0.000,
            0.000,
            8.000,
            5.000,
            6.000,
            9.000,
            9.000,
            7.000,
            0.000,
        ],
    ).tobytes()
    # representing the key inverse matrix as a 1D array of bytes
    byte_inv_key_matrix: bytes = array.array(
        "d",
        [
            0.087698730443907,
            0.106508423872910,
            -0.035837889522160,
            -0.018212614575464,
            0.029282205872323,
            0.009768535961213,
            0.051022092452304,
            -0.002600159007516,
            0.062599483798891,
            -0.020588660945658,
            -0.005731646667785,
            -0.109625191395912,
            -0.006932407372092,
            -0.056202668885562,
            -0.075318484801680,
            0.014708766520769,
            -0.022928256564172,
            -0.026683449299678,
            -0.011012588526442,
            0.129942414512966,
            -0.122921871300045,
            -0.043058741765130,
            -0.117420500612853,
            -0.140391873840202,
            -0.071045583264847,
            -0.034148665820787,
            -0.095666764302039,
            0.234091140082102,
            0.027357920334586,
            0.072726676711471,
            0.065330793324812,
            0.030966972897445,
            -0.218268560384352,
            -0.167198025185273,
            0.018741969126614,
            0.134524170075639,
            -0.321465832541972,
            -0.166586732147428,
            0.039385178742807,
            -0.113346935522171,
            -0.185692852729154,
            -0.043259247663190,
            -0.076549003088936,
            0.573616991323091,
            0.104219031977534,
            0.246544562428294,
            0.177605218056100,
            -0.134494179895595,
            -0.074234710142859,
            -0.152484831242658,
            0.032888774006722,
            0.126780472517150,
            -0.280349992738819,
            -0.177762951540922,
            0.068628817353806,
            -0.051217841640809,
            -0.180654642158176,
            -0.011766502223790,
            -0.080775821814310,
            0.379125349840351,
            0.048682798429393,
            0.251118885929070,
            0.025753297544241,
            -0.015741279938887,
            -0.107282379497940,
            -0.076473612678836,
            0.048411952177752,
            0.128387746395734,
            -0.218476883182669,
            -0.182054566825948,
            0.015297614620229,
            -0.071068523564674,
            -0.173515463207588,
            -0.004127099161250,
            -0.106414518336578,
            0.363864949305460,
            0.024524217055173,
            0.165306494873899,
            0.163356977791568,
            -0.035033674480292,
            0.277288909540715,
            0.191426836794975,
            0.115975544752238,
            -0.300809424418599,
            0.353820685363440,
            0.206982195506894,
            0.135654125071293,
            0.381774054614345,
            0.313562376027531,
            0.069054897975148,
            -0.011797886745698,
            -0.853234848281320,
            0.086056587100296,
            -0.364305268023283,
            -0.618093105304007,
            0.253957528660826,
            0.038358445191113,
            -0.000546407470896,
            -0.073465777300804,
            -0.033200515562292,
            -0.020621719941806,
            0.046779969176516,
            -0.057290779719178,
            -0.095971425211909,
            -0.009648470448360,
            0.006680795638773,
            0.001875819452453,
            0.062297723542825,
            -0.005182609330966,
            0.040283770455199,
            0.144418033011726,
            -0.055272938421632,
            0.241341634348029,
            0.173795889482842,
            -0.037558951477139,
            -0.142555330724481,
            0.384872718455622,
            0.238727072083511,
            -0.012025720907547,
            0.205726531015318,
            0.215305804451694,
            0.050086219117152,
            0.058130045507594,
            -0.741794720895175,
            0.050078370236749,
            -0.310037624023072,
            -0.430832649690117,
            0.179950027829876,
            0.171381216925833,
            0.086060780454874,
            -0.042565007877466,
            -0.078956143623505,
            0.327447146261980,
            0.206393272411101,
            -0.099952932487210,
            0.087552045773402,
            0.173129037727576,
            0.018397910434386,
            0.086685394445941,
            -0.429207905148962,
            -0.134850123674970,
            -0.238397133799728,
            -0.059141482129532,
            0.042322030383679,
            -0.288768790079429,
            -0.180939915747826,
            0.014729697120086,
            0.167827000966843,
            -0.432864619931572,
            -0.272139265354751,
            -0.055798856798054,
            -0.158129080251415,
            -0.179029372582232,
            -0.057409513342173,
            -0.107043502580043,
            0.743098244369843,
            0.075665395931411,
            0.366662136199027,
            0.301325496735494,
            -0.127959853885404,
            0.176761191401067,
            0.163276217872526,
            -0.090326263481081,
            -0.179551087083123,
            0.363256815341333,
            0.329970109430809,
            -0.051879221066062,
            0.256728747731346,
            0.277043384431290,
            0.104113728292426,
            0.139981371677002,
            -0.742130479625641,
            -0.034524073033884,
            -0.343286483781855,
            -0.306301246917888,
            0.117604350114848,
            -0.145793544926800,
            -0.103188494699912,
            0.058788410241278,
            0.051655038640426,
            -0.264038008105031,
            -0.203541647757149,
            0.090418018220672,
            -0.064107759386820,
            -0.219857426756124,
            -0.016087922861208,
            -0.104557302929551,
            0.488954502811962,
            0.057922132921064,
            0.258682714654372,
            0.111924825898909,
            -0.052708836311705,
            0.347740013692901,
            0.186040292334817,
            0.031705891858216,
            -0.245707324109423,
            0.427598565702216,
            0.270498331607873,
            0.111400473365868,
            0.327817668038880,
            0.302461445968564,
            0.027512957314741,
            -0.060711514345127,
            -0.925728053394680,
            -0.033117806958892,
            -0.380932346698436,
            -0.493071060049599,
            0.328947236201250,
            -0.173318365340601,
            -0.077142569984113,
            -0.076310560438528,
            0.089225994308972,
            -0.002018880643991,
            -0.013163178758400,
            -0.064330936170142,
            -0.237122798059981,
            -0.172523534080677,
            -0.064784833527950,
            0.277209132093551,
            0.334394267761285,
            -0.120700446096625,
            0.092203859487363,
            0.485868651300583,
            -0.262678175365571,
            0.051245491573803,
            0.047735585799314,
            0.019889459157673,
            -0.055381465402088,
            0.171358401700705,
            0.049314885561074,
            -0.021834316287122,
            0.033901985721205,
            0.121062561797019,
            0.095099592970483,
            0.052994957136868,
            -0.246427467822199,
            -0.029773768604971,
            -0.153276054566094,
            -0.084954401825375,
            0.052024137604019,
            -0.153612088210597,
            -0.058212221217499,
            0.096467473348521,
            0.129389831134947,
            -0.166369564539914,
            -0.163654572235491,
            -0.019395649590667,
            -0.140682220131554,
            -0.071530405390647,
            -0.016836777394500,
            -0.063409311447827,
            0.372333201408698,
            -0.061510980613705,
            0.172726336659603,
            0.223722169457708,
            -0.120402896064248,
        ],
    ).tobytes()
    upper_case_alphabet: str = string.ascii_uppercase

    def __init__(self):
        # The key and inverse key are initialized using a memoryview object to avoid unnecessary data copying.
        self.key: list = memoryview(self.byte_key_matrix).cast("d", shape=(16, 16)).tolist()
        self.inv_key: list = memoryview(self.byte_inv_key_matrix).cast("d", shape=(16, 16)).tolist()
        self.module: int = 26
        self.digraph_size: int = len(self.key)

    def padding_out_text(self, plaintext: str) -> str:
        """
        Pad the plaintext with "X" characters to match the digraph size.

        To run the doctests: pytest --doctest-modules -vvs <filename>.py

        >>> MatrixEncryption().padding_out_text("HELLO")
        'HELLOXXXXXXXXXXX'
        >>> MatrixEncryption().padding_out_text("HELLOXXXXXXXXXXX")
        'HELLOXXXXXXXXXXX'
        """
        padding_size: int = (
            self.digraph_size - (len(plaintext) % self.digraph_size) if len(plaintext) % self.digraph_size != 0 else 0
        )
        return plaintext + "X" * padding_size

    def convert_to_vector(self, digraph_plaintext: str) -> list[list]:
        """
        Convert the digraph plaintext to a vector of ASCII values.
        """
        return [[self.upper_case_alphabet.index(char) for char in digraph_plaintext]]

    def convert_to_block(self, digraph_vector: list[list]) -> str:
        """
        Convert the digraph vector to a string of characters.
        """
        return "".join([self.upper_case_alphabet[int(val)] for val in digraph_vector[0]])

    def matrix_multiply(self, digraph_vector: list[list], matrix: list[list]) -> list:
        """
        Multiply the digraph vector by the matrix (either the key or inverse key)
        """
        if len(digraph_vector[0]) != len(matrix):
            raise ValueError("The number of columns in the digraph vector must match the number of rows in the matrix.")

        result: list[list] = [[0 for _ in range(len(matrix[0]))] for _ in range(len(digraph_vector))]
        for i in range(len(digraph_vector)):
            for j in range(len(matrix[0])):
                for k in range(len(matrix)):
                    result[i][j] += digraph_vector[i][k] * matrix[k][j]
                result[i][j] %= self.module
        return result

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt the plaintext using the Hill Cipher.

        - The Encryption Algorithm:
        1. Separate the plaintext from left to right into some number k of groups (polygraphs) of n letters each.
            If you run out of letters when forming the final group, repeat "X" letter as many times as needed
            to fill out that final group to n letters.
        2. Replace each letter by the corresponding number of its position (from 0 through m − 1) in the alphabet
            to get k groups of n integers each.
        3. Reshape each of the k groups of integers into an n-row column vector
            and in turn multiply A by each of those k column vectors modulo m.
        4. After arranging all k of the resulting product n-row column vectors in order into a single (k · n)-vector,
            replace each of these k · n entries with the corresponding letter of the alphabet.
            The result is the ciphertext corresponding to the original plaintext.
        """
        # Remove all non-alphabetic characters and convert to uppercase.
        plaintext = "".join([char.upper() for char in plaintext if char.isalpha()])
        padded_plaintext: str = self.padding_out_text(plaintext)
        ciphertext: list[str] = [""] * len(padded_plaintext)

        for i in range(0, len(padded_plaintext), self.digraph_size):
            digraph_plaintext: str = padded_plaintext[i : i + self.digraph_size]
            # Convert the digraph plaintext to a vector of ASCII values.
            digraph_vector: list[list] = self.convert_to_vector(digraph_plaintext)
            # Multiply the digraph vector by the key matrix.
            digraph_ciphertext: list = self.matrix_multiply(digraph_vector, self.key)
            ciphertext[i : i + self.digraph_size] = self.convert_to_block(digraph_ciphertext)

        return "".join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt the ciphertext using the Hill Cipher.
        - The Decryption Algorithm:
            the transformation from ciphertext back to plaintext is just the inverse of the original transformation
            from plaintext to ciphertext.
            In other words, if a Hill cipher has key matrix A, then the inverse transformation is the Hill cipher
            whose key matrix is inv(A), the inverse of A modulo m.
        """
        plain_text: list[str] = [""] * len(ciphertext)
        for i in range(0, len(ciphertext), self.digraph_size):
            digraph_ciphertext: str = ciphertext[i : i + self.digraph_size]
            # Convert the digraph ciphertext to a vector of ASCII values.
            digraph_vector: list[list] = self.convert_to_vector(digraph_ciphertext)
            # Multiply the digraph vector by the inverse key matrix.
            digraph_plaintext: list = self.matrix_multiply(digraph_vector, self.inv_key)
            plain_text[i : i + self.digraph_size] = self.convert_to_block(digraph_plaintext)

        return "".join(plain_text)


class ReverseEncryption(CryptoAlgorithm):
    """
    Reverse Encryption Algorithm.
    """

    def __init__(self, encrypt_url: str, decrypt_url: str):
        self.encrypt_url = encrypt_url or "http://backendtask.robustastudio.com/encode"
        self.decrypt_url = decrypt_url or "http://backendtask.robustastudio.com/decode"

    def encrypt(self, plain_text: str) -> str:
        headers = {"Content-Type": "application/json"}
        response = httpx.post(self.encrypt_url, headers=headers, json={"text": plain_text})
        return response.json().get("encoded_text", "")

    def decrypt(self, cipher_text: str) -> str:
        headers = {"Content-Type": "application/json"}
        response = httpx.post(self.decrypt_url, headers=headers, json={"text": cipher_text})
        return response.json().get("decoded_text", "")


class CryptoAlgorithmFactory:
    """
    Factory class for dynamically creating crypto algorithm instances.

    This factory class provides a convenient way to create different crypto algorithm instances
    """

    @staticmethod
    def create_algorithm(algorithm_name: str, **kwargs):
        """
        Create a crypto algorithm instance based on the specified algorithm name and optional arguments.
        Returns:
        - CryptoAlgorithm: An instance of the specified crypto algorithm.
        """
        if algorithm_name == "shift":
            shift = int(kwargs.get("shift", 3))
            return ShiftEncryption(shift)
        elif algorithm_name == "matrix":
            return MatrixEncryption()
        elif algorithm_name == "reverse":
            encrypt_url = "https://encryption-api-five.vercel.app/encode"
            decrypt_url = "https://encryption-api-five.vercel.app/decode"
            return ReverseEncryption(encrypt_url=encrypt_url, decrypt_url=decrypt_url)
        else:
            raise ValueError(f"Invalid algorithm name: {algorithm_name}")
