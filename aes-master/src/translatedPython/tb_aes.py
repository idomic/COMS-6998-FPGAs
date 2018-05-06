from time import time
from aes import aes
from myhdl import *


# //------------------------------------------------------------------
# // Test module.
# //------------------------------------------------------------------
def tb_aes():
    # //----------------------------------------------------------------
    # // Internal constant and parameter definitions.
    # //----------------------------------------------------------------
    DEBUG = 0
    CLK_HALF_PERIOD = 1
    CLK_PERIOD = 2 * CLK_HALF_PERIOD

    # // The DUT address map.
    ADDR_NAME0 = intbv(0, min = 0, max = 255)
    ADDR_NAME1 = intbv(1, min = 0, max = 255)
    ADDR_VERSION = intbv(2, min = 0, max = 255)

    ADDR_CTRL = intbv(8, min = 0, max = 255)
    CTRL_INIT_BIT = 0
    CTRL_NEXT_BIT = 1
    CTRL_ENCDEC_BIT = 2
    CTRL_KEYLEN_BIT = 3

    ADDR_STATUS = intbv(9, min = 0, max = 255)
    STATUS_READY_BIT = 0
    STATUS_VALID_BIT = 1

    ADDR_CONFIG = intbv(10, min = 0, max = 255)

    ADDR_KEY0 = intbv(16, min = 0, max = 255)
    ADDR_KEY1 = intbv(17, min = 0, max = 255)
    ADDR_KEY2 = intbv(18, min = 0, max = 255)
    ADDR_KEY3 = intbv(19, min = 0, max = 255)
    ADDR_KEY4 = intbv(20, min = 0, max = 255)
    ADDR_KEY5 = intbv(21, min = 0, max = 255)
    ADDR_KEY6 = intbv(22, min = 0, max = 255)
    ADDR_KEY7 = intbv(23, min = 0, max = 255)

    ADDR_BLOCK0 = intbv(32, min = 0, max = 255)
    ADDR_BLOCK1 = intbv(33, min = 0, max = 255)
    ADDR_BLOCK2 = intbv(34, min = 0, max = 255)
    ADDR_BLOCK3 = intbv(35, min = 0, max = 255)

    ADDR_RESULT0 = intbv(48, min = 0, max = 255)
    ADDR_RESULT1 = intbv(49, min = 0, max = 255)
    ADDR_RESULT2 = intbv(50, min = 0, max = 255)
    ADDR_RESULT3 = intbv(51, min = 0, max = 255)

    AES_128_BIT_KEY = 0
    AES_256_BIT_KEY = 1

    AES_DECIPHER = 0
    AES_ENCIPHER = 1

    # //----------------------------------------------------------------
    # // Register and Wire declarations.
    # //----------------------------------------------------------------
    cycle_ctr = Signal(intbv()[32:])  # reg [31 : 0]  cycle_ctr;
    error_ctr = Signal(intbv()[32:])  # reg [31 : 0]  error_ctr;
    tc_ctr = Signal(intbv()[32:])  # reg [31 : 0]  tc_ctr;

    read_data = Signal(intbv()[32:])  # reg [31 : 0]  read_data;
    result_data = Signal(intbv()[128:])  # reg [127 : 0] result_data;

    tb_clk = Signal(bool(0))  # reg           tb_clk;
    tb_reset_n = Signal(bool(0))  # reg           tb_reset_n;
    tb_cs = Signal(bool(0))  # reg           tb_cs;
    tb_we = Signal(bool(0))  # reg           tb_we;
    tb_address = Signal(intbv()[8:])  # reg [7  : 0]  tb_address;
    tb_write_data = Signal(intbv()[32:])  # reg [31 : 0]  tb_write_data;
    tb_read_data = Signal(intbv()[32:])  # wire [31 : 0] tb_read_data;

    # //----------------------------------------------------------------
    # // Device Under Test.
    # //----------------------------------------------------------------
    # dut = aes(tb_clk, tb_reset_n, tb_cs, tb_we, tb_address, tb_write_data, tb_read_data)

    # Uncomment this line to generate verilog during simulation
    dut = toVerilog(aes, tb_clk, tb_reset_n, tb_cs, tb_we, tb_address, tb_write_data, tb_read_data)


    # //----------------------------------------------------------------
    # // clk_gen
    # //
    # // Always running clock generator process.
    # //----------------------------------------------------------------
    @always(delay(CLK_HALF_PERIOD))
    def clk_gen():
        tb_clk.next = not tb_clk

    # //----------------------------------------------------------------
    # // sys_monitor()
    # //
    # // An always running process that creates a cycle counter and
    # // conditionally displays information about the DUT.
    # //----------------------------------------------------------------
    @instance
    def sys_monitor():
        while True:
            yield delay(CLK_PERIOD)
            cycle_ctr.next[:] = cycle_ctr + 1
            # (CLK_PERIOD);

    # //----------------------------------------------------------------
    # // dump_dut_state()
    # //
    # // Dump the state of the dump when needed.
    # //----------------------------------------------------------------
    @always(cycle_ctr)
    def dump_dut_state():
        print("cycle: 0x%016x" % cycle_ctr)
        print("State of DUT")
        print("------------")
        print("ctrl_reg:   init   = 0x%01x, next   = 0x%01x" % (dut[1].init_reg, dut[1].next_reg))
        print("config_reg: encdec = 0x%01x, length = 0x%01x " % (dut[1].encdec_reg, dut[1].keylen_reg))
        print("")
        print("block: 0x%08x, 0x%08x, 0x%08x, 0x%08x" %
              ( dut[1].block_reg[0], dut[1].block_reg[1], dut[1].block_reg[2], dut[1].block_reg[3]))
        print("")


    # //----------------------------------------------------------------
    # // reset_dut()
    # //
    # // Toggle reset to put the DUT into a well known state.
    # //----------------------------------------------------------------
    def reset_dut():
        print("*** Toggle reset.")
        tb_reset_n.next = 0
        yield delay(2 * CLK_PERIOD)
        # (2 * CLK_PERIOD);
        tb_reset_n.next = 1
        print("")

    # //----------------------------------------------------------------
    # // display_test_results()
    # //
    # // Display the accumulated test results.
    # //----------------------------------------------------------------
    def display_test_results():
        if (error_ctr == 0):
            print("*** All %02d test cases completed successfully" % int(tc_ctr))
        else:
            print("*** %02d tests completed - %02d test cases did not complete successfully." %
                  (int(tc_ctr), int(error_ctr)))

    # //----------------------------------------------------------------
    # // init_sim()
    # //
    # // Initialize all counters and testbed functionality as well
    # // as setting the DUT inputs to defined values.
    # //----------------------------------------------------------------
    def init_sim():
        cycle_ctr.next[:] = 0
        error_ctr.next[:] = 0
        tc_ctr.next[:] = 0

        tb_clk.next = 0
        tb_reset_n.next = 1
        tb_cs.next = 0
        tb_we.next = 0
        tb_address.next[:] = 0
        tb_write_data.next[:] = 0  # tb_write_data = 32'h0;

    # //----------------------------------------------------------------
    # // write_word()
    # //
    # // Write the given word to the DUT using the DUT interface.
    # //----------------------------------------------------------------
    def write_word(address, word):
        if (DEBUG):
            print("*** Writing 0x%08x to 0x%02x." % (word, address))
            print("")

        tb_address.next[:] = address
        tb_write_data.next[:] = word
        tb_cs.next = 1
        tb_we.next = 1
        yield delay(2 * CLK_PERIOD)
        # (2 * CLK_PERIOD);
        tb_cs.next = 0
        tb_we.next = 0

    # //----------------------------------------------------------------
    # // write_block()
    # //
    # // Write the given block to the dut.
    # //----------------------------------------------------------------
    def write_block(block):
        yield write_word(ADDR_BLOCK0, block[127:96])
        yield write_word(ADDR_BLOCK1, block[95:64])
        yield write_word(ADDR_BLOCK2, block[63:32])
        yield write_word(ADDR_BLOCK3, block[31:0])

    # //----------------------------------------------------------------
    # // read_word()
    # //
    # // Read a data word from the given address in the DUT.
    # // the word read will be available in the global variable
    # // read_data.
    # //----------------------------------------------------------------
    def read_word(address):
        tb_address.next[:] = address
        tb_cs.next = 1
        tb_we.next = 0

        yield delay(CLK_PERIOD)  # (CLK_PERIOD);

        read_data.val[:] = tb_read_data
        tb_cs.next = 0

        if (DEBUG):
            print("*** Reading 0x%08x from 0x%02x." % (read_data, address))
            print("")

    # //----------------------------------------------------------------
    # // read_result()
    # //
    # // Read the result block in the dut.
    # //----------------------------------------------------------------
    def read_result():

        yield read_word(ADDR_RESULT0)
        result_data.val[127:96] = read_data
        yield read_word(ADDR_RESULT1)
        result_data.val[95:64] = read_data
        yield read_word(ADDR_RESULT2)
        result_data.val[63:32] = read_data
        yield read_word(ADDR_RESULT3)
        result_data.val[31:0] = read_data

    # //----------------------------------------------------------------
    # // init_key()
    # //
    # // init the key in the dut by writing the given key and
    # // key length and then trigger init processing.
    # //----------------------------------------------------------------
    def init_key(key, key_length):
        if (DEBUG):
            print("key length: 0x%01x" % key_length)
            print("Initializing key expansion for key: 0x%016x" % key)

        yield write_word(ADDR_KEY0, key[255:224])
        yield write_word(ADDR_KEY1, key[223:192])
        yield write_word(ADDR_KEY2, key[191:160])
        yield write_word(ADDR_KEY3, key[159:128])
        yield write_word(ADDR_KEY4, key[127:96])
        yield write_word(ADDR_KEY5, key[95:64])
        yield write_word(ADDR_KEY6, key[63:32])
        yield write_word(ADDR_KEY7, key[31:0])

        if (key_length):
            yield write_word(ADDR_CONFIG, 2)
        else:
            yield write_word(ADDR_CONFIG, 0)

        yield write_word(ADDR_CTRL, 1)
        yield delay(100 * CLK_PERIOD)
        # (100 * CLK_PERIOD);

    # //----------------------------------------------------------------
    # // ecb_mode_single_block_test()
    # //
    # // Perform ECB mode encryption or decryption single block test.
    # //----------------------------------------------------------------
    def ecb_mode_single_block_test(tc_number, encdec, key, key_length, block, expected):
        print("*** TC %0d ECB mode test started." % tc_number)
        tc_ctr.next[:] = tc_ctr + 1

        yield init_key(key, key_length)
        yield write_block(block)

        yield write_word(ADDR_CONFIG, (intbv(0, min = 0, max = 31) + (key_length << 1) + encdec));
        yield write_word(ADDR_CTRL, 2);
        yield delay(100 * CLK_PERIOD)
        # (100 * CLK_PERIOD);

        yield read_result();

        if (result_data == expected):
            print("*** TC %0d successful." % tc_number)
            print("")
            pass
        else:
            print("*** ERROR: TC %0d NOT successful." % tc_number)
            print("Expected: 0x%x" % expected)
            print("Got:      0x%x" % result_data)
            print("")

            error_ctr.next[:] = error_ctr + 1

    # //----------------------------------------------------------------
    # // aes_test()
    # //
    # // Main test task will perform complete NIST test of AES.
    # //----------------------------------------------------------------
    @instance
    def aes_test():
        print("   -= Testbench for AES started =-")
        print("    ==============================")
        print("")

        # Initialize the system
        init_sim()

        # Reset
        yield reset_dut()

        # Not here. Check name and version
        # yield check_name_version()

        nist_aes128_key = intbv()[256:]  # reg [255 : 0] nist_aes128_key;
        nist_aes256_key = intbv()[256:]  # reg [255 : 0] nist_aes256_key;
        nist_plaintext0 = intbv()[128:]  # reg [127 : 0] nist_plaintext0;
        nist_plaintext1 = intbv()[128:]  # reg [127 : 0] nist_plaintext1;
        nist_plaintext2 = intbv()[128:]  # reg [127 : 0] nist_plaintext2;
        nist_plaintext3 = intbv()[128:]  # reg [127 : 0] nist_plaintext3;

        nist_ecb_128_enc_expected0 = intbv()[128:]  # reg [127 : 0] nist_ecb_128_enc_expected0;
        nist_ecb_128_enc_expected1 = intbv()[128:]  # reg [127 : 0] nist_ecb_128_enc_expected1;
        nist_ecb_128_enc_expected2 = intbv()[128:]  # reg [127 : 0] nist_ecb_128_enc_expected2;
        nist_ecb_128_enc_expected3 = intbv()[128:]  # reg [127 : 0] nist_ecb_128_enc_expected3;

        nist_ecb_256_enc_expected0 = intbv()[128:]  # reg [127 : 0] nist_ecb_256_enc_expected0;
        nist_ecb_256_enc_expected1 = intbv()[128:]  # reg [127 : 0] nist_ecb_256_enc_expected1;
        nist_ecb_256_enc_expected2 = intbv()[128:]  # reg [127 : 0] nist_ecb_256_enc_expected2;
        nist_ecb_256_enc_expected3 = intbv()[128:]  # reg [127 : 0] nist_ecb_256_enc_expected3;

        nist_aes128_key[:] = 0x2b7e151628aed2a6abf7158809cf4f3c00000000000000000000000000000000
        nist_aes256_key[:] = 0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4

        nist_plaintext0[:] = 0x6bc1bee22e409f96e93d7e117393172a
        nist_plaintext1[:] = 0xae2d8a571e03ac9c9eb76fac45af8e51
        nist_plaintext2[:] = 0x30c81c46a35ce411e5fbc1191a0a52ef
        nist_plaintext3[:] = 0xf69f2445df4f9b17ad2b417be66c3710

        nist_ecb_128_enc_expected0[:] = 0x3ad77bb40d7a3660a89ecaf32466ef97
        nist_ecb_128_enc_expected1[:] = 0xf5d3d58503b9699de785895a96fdbaaf
        nist_ecb_128_enc_expected2[:] = 0x43b1cd7f598ece23881b00e3ed030688
        nist_ecb_128_enc_expected3[:] = 0x7b0c785e27e8ad3f8223207104725dd4

        nist_ecb_256_enc_expected0[:] = 0xf3eed1bdb5d2a03c064b5a7e3db181f8
        nist_ecb_256_enc_expected1[:] = 0x591ccb10d410ed26dc5ba74a31362870
        nist_ecb_256_enc_expected2[:] = 0xb6ed21b99ca6f4f9f153e7b1beafed1d
        nist_ecb_256_enc_expected3[:] = 0x23304b7a39f9f3ff067d8d8f9e24ecc7

        print("ECB 128 bit key tests")
        print("---------------------")
        print("DUT")
        # dump_dut_state()
        yield ecb_mode_single_block_test(0x01, AES_ENCIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_plaintext0, nist_ecb_128_enc_expected0);

        yield ecb_mode_single_block_test(0x02, AES_ENCIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_plaintext1, nist_ecb_128_enc_expected1);

        yield ecb_mode_single_block_test(0x03, AES_ENCIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_plaintext2, nist_ecb_128_enc_expected2);

        yield ecb_mode_single_block_test(0x04, AES_ENCIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_plaintext3, nist_ecb_128_enc_expected3);

        yield ecb_mode_single_block_test(0x05, AES_DECIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_ecb_128_enc_expected0, nist_plaintext0)

        yield ecb_mode_single_block_test(0x06, AES_DECIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_ecb_128_enc_expected1, nist_plaintext1)

        yield ecb_mode_single_block_test(0x07, AES_DECIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_ecb_128_enc_expected2, nist_plaintext2)

        yield ecb_mode_single_block_test(0x08, AES_DECIPHER, nist_aes128_key, AES_128_BIT_KEY,
                                         nist_ecb_128_enc_expected3, nist_plaintext3)

        yield delay(CLK_PERIOD)

        print("")
        print("ECB 256 bit key tests")
        print("---------------------")
        yield ecb_mode_single_block_test(0x10, AES_ENCIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_plaintext0, nist_ecb_256_enc_expected0)

        yield ecb_mode_single_block_test(0x11, AES_ENCIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_plaintext1, nist_ecb_256_enc_expected1)

        yield ecb_mode_single_block_test(0x12, AES_ENCIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_plaintext2, nist_ecb_256_enc_expected2)

        yield ecb_mode_single_block_test(0x13, AES_ENCIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_plaintext3, nist_ecb_256_enc_expected3)

        yield ecb_mode_single_block_test(0x14, AES_DECIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_ecb_256_enc_expected0, nist_plaintext0);

        yield ecb_mode_single_block_test(0x15, AES_DECIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_ecb_256_enc_expected1, nist_plaintext1);

        yield ecb_mode_single_block_test(0x16, AES_DECIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_ecb_256_enc_expected2, nist_plaintext2);

        yield ecb_mode_single_block_test(0x17, AES_DECIPHER, nist_aes256_key, AES_256_BIT_KEY,
                                         nist_ecb_256_enc_expected3, nist_plaintext3)

        # Display results and finish up
        yield delay(CLK_PERIOD)
        display_test_results()

        print("")
        print("*** AES simulation done. ***")

        raise StopSimulation

    return dut, aes_test, clk_gen, sys_monitor


# //======================================================================
# // EOF tb_aes.v
# //======================================================================



def test_bench():
    start = time()
    tb = tb_aes()
    # print ("This is tb")
    # print(tb)
    sim = Simulation(tb)
    print("Synthesised!")
    print(time() - start)
    sim.run()
    print(time() - start)


test_bench()

# For generating a waveform
# tb = traceSignals(tb_aes)
# sim = Simulation(tb)
# sim.run()
