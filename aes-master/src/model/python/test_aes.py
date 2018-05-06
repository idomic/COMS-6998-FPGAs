from myhdl import *
from time import time
from aes import *
#-------------------------------------------------------------------
# test_aes()
#
# Test the AES implementation with 128 and 256 bit keys.
#-------------------------------------------------------------------

def testbench():
    nist_aes128_key = (0x2b7e1516, 0x28aed2a6, 0xabf71588, 0x09cf4f3c)
    nist_aes256_key = (0x603deb10, 0x15ca71be, 0x2b73aef0, 0x857d7781,
                       0x1f352c07, 0x3b6108d7, 0x2d9810a3, 0x0914dff4)

    nist_plaintext0 = (0x6bc1bee2, 0x2e409f96, 0xe93d7e11, 0x7393172a)
    nist_plaintext1 = (0xae2d8a57, 0x1e03ac9c, 0x9eb76fac, 0x45af8e51)
    nist_plaintext2 = (0x30c81c46, 0xa35ce411, 0xe5fbc119, 0x1a0a52ef)
    nist_plaintext3 = (0xf69f2445, 0xdf4f9b17, 0xad2b417b, 0xe66c3710)

    nist_exp128_0 = (0x3ad77bb4, 0x0d7a3660, 0xa89ecaf3, 0x2466ef97)
    nist_exp128_1 = (0xf5d3d585, 0x03b9699d, 0xe785895a, 0x96fdbaaf)
    nist_exp128_2 = (0x43b1cd7f, 0x598ece23, 0x881b00e3, 0xed030688)
    nist_exp128_3 = (0x7b0c785e, 0x27e8ad3f, 0x82232071, 0x04725dd4)

    nist_exp256_0 = (0xf3eed1bd, 0xb5d2a03c, 0x064b5a7e, 0x3db181f8)
    nist_exp256_1 = (0x591ccb10, 0xd410ed26, 0xdc5ba74a, 0x31362870)
    nist_exp256_2 = (0xb6ed21b9, 0x9ca6f4f9, 0xf153e7b1, 0xbeafed1d)
    nist_exp256_3 = (0x23304b7a, 0x39f9f3ff, 0x067d8d8f, 0x9e24ecc7)


    print("Doing block encryption.")
    enc_result128_0 = aes_encipher_block(nist_aes128_key, nist_plaintext0)
    enc_result128_1 = aes_encipher_block(nist_aes128_key, nist_plaintext1)
    enc_result128_2 = aes_encipher_block(nist_aes128_key, nist_plaintext2)
    enc_result128_3 = aes_encipher_block(nist_aes128_key, nist_plaintext3)

    enc_result256_0 = aes_encipher_block(nist_aes256_key, nist_plaintext0)
    enc_result256_1 = aes_encipher_block(nist_aes256_key, nist_plaintext1)
    enc_result256_2 = aes_encipher_block(nist_aes256_key, nist_plaintext2)
    enc_result256_3 = aes_encipher_block(nist_aes256_key, nist_plaintext3)

    print("Doing block decryption.")
    dec_result128_0 = aes_decipher_block(nist_aes128_key, nist_exp128_0)
    dec_result128_1 = aes_decipher_block(nist_aes128_key, nist_exp128_1)
    dec_result128_2 = aes_decipher_block(nist_aes128_key, nist_exp128_2)
    dec_result128_3 = aes_decipher_block(nist_aes128_key, nist_exp128_3)

    dec_result256_0 = aes_decipher_block(nist_aes256_key, nist_exp256_0)
    dec_result256_1 = aes_decipher_block(nist_aes256_key, nist_exp256_1)
    dec_result256_2 = aes_decipher_block(nist_aes256_key, nist_exp256_2)
    dec_result256_3 = aes_decipher_block(nist_aes256_key, nist_exp256_3)

    tc_errors = 0
    tc        = 0

    if VERBOSE:
        print("   AES Encipher tests")
        print("   ==================")

        print("Test 0 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_plaintext0)
        tc_errors += check_block(nist_exp128_0, enc_result128_0)
        tc += 1

        print("Test 1 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_plaintext1)
        tc_errors += check_block(nist_exp128_1, enc_result128_1)
        tc += 1

        print("Test 2 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_plaintext2)
        tc_errors += check_block(nist_exp128_2, enc_result128_2)
        tc += 1

        print("Test 3 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_plaintext3)
        tc_errors += check_block(nist_exp128_3, enc_result128_3)
        tc += 1

        print("Test 0 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_plaintext0)
        tc_errors += check_block(nist_exp256_0, enc_result256_0)
        tc += 1

        print("Test 1 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_plaintext1)
        tc_errors += check_block(nist_exp256_1, enc_result256_1)
        tc += 1

        print("Test 2 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_plaintext2)
        tc_errors += check_block(nist_exp256_2, enc_result256_2)
        tc += 1

        print("Test 3 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_plaintext3)
        tc_errors += check_block(nist_exp256_3, enc_result256_3)
        tc += 1


        print("")
        print("   AES Decipher tests")
        print("   ==================")

        print("Test 0 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_exp128_0)
        tc_errors += check_block(nist_plaintext0, dec_result128_0)
        tc += 1

        print("Test 1 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_exp128_1)
        tc_errors += check_block(nist_plaintext1, dec_result128_1)
        tc += 1

        print("Test 2 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_exp128_2)
        tc_errors += check_block(nist_plaintext2, dec_result128_2)
        tc += 1

        print("Test 3 for AES-128.")
        print("Key:")
        print_key(nist_aes128_key)
        print("Block in:")
        print_block(nist_exp128_3)
        tc_errors += check_block(nist_plaintext3, dec_result128_3)
        tc += 1

        print("Test 0 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_exp256_0)
        tc_errors += check_block(nist_plaintext0, dec_result256_0)
        tc += 1

        print("Test 1 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_exp256_1)
        tc_errors += check_block(nist_plaintext1, dec_result256_1)
        tc += 1

        print("Test 2 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_exp256_2)
        tc_errors += check_block(nist_plaintext2, dec_result256_2)
        tc += 1

        print("Test 3 for AES-256.")
        print("Key:")
        print_key(nist_aes256_key)
        print("Block in:")
        print_block(nist_exp256_3)
        tc_errors += check_block(nist_plaintext3, dec_result256_3)
        tc += 1

        print("Number of test cases executed: %d" % tc)
        if (tc_errors == 0):
            print("All test cases OK.")
        else:
            print("Number of failing test cases: %d" % tc_errors)


#-------------------------------------------------------------------
# main()
#
# If executed tests the ChaCha class using known test vectors.
#-------------------------------------------------------------------

def test_bench():
    print("Testing the AES cipher model")
    print("============================")
    print
    start = time()
    tb = testbench()
    sim = Simulation(tb)
    sim.run()
    #testbench()
    print(time() - start)


test_bench()