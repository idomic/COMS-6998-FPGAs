from myhdl import *

def aes_encipher_block(clk, reset_n, next, keylen, round, round_key, sboxw, new_sboxw, block, new_block, ready):
						 #  input wire            clk,
						 #  input wire            reset_n,
						 #
						 #  input wire            next,
						 #
						 #  input wire            keylen,
						 #  output wire [3 : 0]   round,
						 #  input wire [127 : 0]  round_key,
						 #
						 #  output wire [31 : 0]  sboxw,
						 #  input wire  [31 : 0]  new_sboxw,
						 #
						 #  input wire [127 : 0]  block,
						 #  output wire [127 : 0] new_block,
						 #  output wire           ready
						 # );


    # //----------------------------------------------------------------
    # // Internal constant and parameter definitions.
    # //----------------------------------------------------------------
    AES_128_BIT_KEY = intbv(0, min = 0, max = 7)
    AES_256_BIT_KEY = intbv(1, min = 0, max = 7)

    AES128_ROUNDS = intbv(10, min = 0, max = 64)
    AES256_ROUNDS = intbv(14, min = 0, max = 64)

    NO_UPDATE = intbv(0, min = 0, max = 48)
    INIT_UPDATE = intbv(1, min = 0, max = 48)
    SBOX_UPDATE = intbv(2, min = 0, max = 48)
    MAIN_UPDATE = intbv(3, min = 0, max = 48)
    FINAL_UPDATE = intbv(4, min = 0, max = 48)

    CTRL_IDLE = intbv(0, min = 0, max = 48)
    CTRL_INIT = intbv(1, min = 0, max = 48)
    CTRL_SBOX = intbv(2, min = 0, max = 48)
    CTRL_MAIN = intbv(3, min = 0, max = 48)
    CTRL_FINAL = intbv(4, min = 0, max = 48)


    # //----------------------------------------------------------------
    # // Round functions with sub functions.
    # //----------------------------------------------------------------

    def gm2(op):
     gm2.next[:] = op[6: 0] ^ 0x0000001b & op[7]  # TODO: gm2 = {op[6 : 0], 1'b0} ^ (8'h1b & {8{op[7]}});
     gm2.next[:] = 0 ^ 0x0000001b & op[7]

    def gm3(op):
     gm3 = gm2(op) ^ op

    def mixw(w):
      b0 = Signal(intbv()[8:])
      b1 = Signal(intbv()[8:])
      b2 = Signal(intbv()[8:])
      b3 = Signal(intbv()[8:])  # reg [7 : 0] b0, b1, b2, b3;

      mb0 = Signal(intbv()[8:])
      mb1 = Signal(intbv()[8:])
      mb2 = Signal(intbv()[8:])
      mb3 = Signal(intbv()[8:])  # reg [7 : 0] mb0, mb1, mb2, mb3;

      b0.next[:] = w[31:24]
      b1.next[:] = w[23:16]
      b2.next[:] = w[15:8]
      b3.next[:] = w[7:0]

      mb0 = gm2(b0) ^ gm3(b1) ^ b2      ^ b3
      mb1 = b0      ^ gm2(b1) ^ gm3(b2) ^ b3
      mb2 = b0      ^ b1      ^ gm2(b2) ^ gm3(b3)
      mb3 = gm3(b0) ^ b1      ^ b2      ^ gm2(b3)

      return mb0, mb1, mb2, mb3


    def mixcolumns(data):
     w0 = Signal(intbv()[32:])  # reg [31 : 0] w0, w1, w2, w3;
     w1 = Signal(intbv()[32:])
     w2 = Signal(intbv()[32:])
     w3 = Signal(intbv()[32:])

     ws0 = Signal(intbv()[32:])  # reg [31 : 0] ws0, ws1, ws2, ws3;
     ws1 = Signal(intbv()[32:])
     ws2 = Signal(intbv()[32:])
     ws3 = Signal(intbv()[32:])

     w0.next[:] = data[127: 96]
     w1.next[:] = data[95: 64]
     w2.next[:] = data[63: 32]
     w3.next[:] = data[31: 0]

     ws0 = mixw(w0)
     ws1 = mixw(w1)
     ws2 = mixw(w2)
     ws3 = mixw(w3)

     return ws0, ws1, ws2, ws3

    def shiftrows(data):
     w0 = Signal(intbv()[32:])  # reg [31 : 0] w0, w1, w2, w3;
     w1 = Signal(intbv()[32:])
     w2 = Signal(intbv()[32:])
     w3 = Signal(intbv()[32:])

     ws0 = Signal(intbv()[32:])  # reg [31 : 0] ws0, ws1, ws2, ws3;
     ws1 = Signal(intbv()[32:])
     ws2 = Signal(intbv()[32:])
     ws3 = Signal(intbv()[32:])

     w0.next[:] = data[127: 96]
     w1.next[:] = data[95: 64]
     w2.next[:] = data[63: 32]
     w3.next[:] = data[31: 0]

     ws0.next[31: 24] = w0[31: 24]  # ws0 = {w0[31 : 24], w1[23 : 16], w2[15 : 08], w3[07 : 00]};
     ws0.next[23: 16] = w1[23: 16]
     ws0.next[15: 8] = w2[15: 8]
     ws0.next[7: 0] = w3[7: 0]

     ws1.next[31: 24] = w1[31: 24]  # ws1 = {w1[31 : 24], w2[23 : 16], w3[15 : 08], w0[07 : 00]};
     ws1.next[23: 16] = w2[23: 16]
     ws1.next[15: 8] = w3[15: 8]
     ws1.next[7: 0] = w0[7: 0]

     ws2.next[31: 24] = w2[31: 24]  # ws2 = {w2[31 : 24], w3[23 : 16], w0[15 : 08], w1[07 : 00]};
     ws2.next[23: 16] = w3[23: 16]
     ws2.next[15: 8] = w0[15: 8]
     ws2.next[7: 0] = w1[7: 0]

     ws3.next[31: 24] = w3[31: 24]  # ws3 = {w3[31 : 24], w0[23 : 16], w1[15 : 08], w2[07 : 00]};
     ws3.next[23: 16] = w0[23: 16]
     ws3.next[15: 8] = w1[15: 8]
     ws3.next[7: 0] = w2[7: 0]

     return ws0, ws1, ws2, ws3


    def addroundkey(data, rkey):
     return data ^ rkey

    # //----------------------------------------------------------------
    # // Registers including update variables and write enable.
    # //----------------------------------------------------------------


    sword_ctr_reg = Signal(intbv()[2:])  # reg [1 : 0]   sword_ctr_reg;
    sword_ctr_new = Signal(intbv()[2:])  # reg [1 : 0]   sword_ctr_new;
    sword_ctr_we = Signal(bool())  # reg           sword_ctr_we;
    sword_ctr_inc = Signal(bool())  # reg           sword_ctr_inc;
    sword_ctr_rst = Signal(bool())  # reg           sword_ctr_rst;

    round_ctr_reg = Signal(intbv()[4:])  # reg [3 : 0]   round_ctr_reg;
    round_ctr_new = Signal(intbv()[4:])  # reg [3 : 0]   round_ctr_new;
    round_ctr_we = Signal(bool())  # reg           round_ctr_we;
    round_ctr_rst = Signal(bool())  # reg           round_ctr_set;
    round_ctr_inc = Signal(bool())  # reg           round_ctr_dec;

    block_new = Signal(intbv()[128:]) # reg [127 : 0] block_new;
    block_w0_reg = Signal(intbv()[32:]) # reg [31 : 0]  block_w0_reg;
    block_w1_reg = Signal(intbv()[32:]) # reg [31 : 0]  block_w1_reg;
    block_w2_reg = Signal(intbv()[32:]) # reg [31 : 0]  block_w2_reg;
    block_w3_reg = Signal(intbv()[32:]) # reg [31 : 0]  block_w3_reg;
    block_w0_we = Signal(bool()) # reg           block_w0_we;
    block_w1_we = Signal(bool()) # reg           block_w1_we;
    block_w2_we = Signal(bool()) # reg           block_w2_we;
    block_w3_we = Signal(bool()) # reg           block_w3_we;

    ready_reg = Signal(bool())  # reg           ready_reg;
    ready_new = Signal(bool())  # reg           ready_new;
    ready_we = Signal(bool())  # reg           ready_we;

    enc_ctrl_reg = Signal(intbv()[3:]) # reg [2 : 0]   dec_ctrl_reg;
    enc_ctrl_new = Signal(intbv()[3:])  # reg [2 : 0]   dec_ctrl_new;
    enc_ctrl_we = Signal(bool()) # reg           dec_ctrl_we;


    # //----------------------------------------------------------------
    # // Wires.
    # //----------------------------------------------------------------

    muxed_sboxw = Signal(intbv()[32:])  # reg [31 : 0] muxed_sboxw;
    update_type = Signal(intbv()[3:])  # reg [2 : 0]   update_type;


    # //----------------------------------------------------------------
    # // Concurrent connectivity for ports etc.
    # //----------------------------------------------------------------
    @always_comb
    def logic():
     round.next[:] = round_ctr_reg #assign round     = round_ctr_reg;
     new_block.next[127:92] = block_w0_reg  # new_block = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};
     new_block.next[91:64] = block_w1_reg
     new_block.next[63:32] = block_w2_reg
     new_block.next[31:00] = block_w3_reg
     ready.next = ready_reg  # assign ready     = ready_reg;
     sboxw.next[:] = muxed_sboxw # assign sboxw     = muxed_sboxw;


    # //----------------------------------------------------------------
    # // reg_update
    # //
    # // Update functionality for all registers in the core.
    # // All registers are positive edge triggered with asynchronous
    # // active low reset. All registers have write enable.
    # //----------------------------------------------------------------


    @always(clk.posedge, reset_n.negedge)  # always @ (posedge clk or negedge reset_n)
    def reg_update():  # begin : reg_update
      if not reset_n:
       block_w0_reg.next[:] = 0  # block_w0_reg  <= 32'h0;
       block_w1_reg.next[:] = 0  # block_w1_reg  <= 32'h0;
       block_w2_reg.next[:] = 0  # block_w2_reg  <= 32'h0;
       block_w3_reg.next[:] = 0  # block_w3_reg  <= 32'h0;
       sword_ctr_reg.next[:] = 0  # sword_ctr_reg <= 2'h0;
       round_ctr_reg.next[:] = 0  # round_ctr_reg <= 4'h0;
       ready_reg.next = 1  # ready_reg     <= 1'b1;
       enc_ctrl_reg.next[:] = CTRL_IDLE  # dec_ctrl_reg  <= CTRL_IDLE;
      else:
        if (block_w0_we):
          block_w0_reg.next[:] = block_new[127: 96]  # block_w0_reg <= block_new[127 : 096];

        if (block_w1_we):
          block_w1_reg.next[:] = block_new[95: 64]  # block_w1_reg <= block_new[095 : 064];

        if (block_w2_we):
          block_w2_reg.next[:] = block_new[63: 32]  # block_w2_reg <= block_new[063 : 032];

        if (block_w3_we):
          block_w3_reg.next[:] = block_new[31: 0]  # block_w3_reg <= block_new[031 : 000];

        if (sword_ctr_we):
          sword_ctr_reg.next[:] = sword_ctr_new  # sword_ctr_reg <= sword_ctr_new;

        if (round_ctr_we):
          round_ctr_reg.next[:] = round_ctr_new  # round_ctr_reg <= round_ctr_new;

        if (ready_we):
          ready_reg.next = ready_new  # ready_reg <= ready_new;

        if (enc_ctrl_we):
          enc_ctrl_reg.next[:] = enc_ctrl_new  # dec_ctrl_reg <= dec_ctrl_new;


    # //----------------------------------------------------------------
    # // round_logic
    # //
    # // The logic needed to implement init, main and final rounds.
    # //----------------------------------------------------------------

    @always(block_new, round_key, round, block_w0_we, block_w3_we, block_w2_we, block_w1_we, update_type, new_sboxw, sword_ctr_reg)
    def round_logic():
      old_b = Signal(intbv()[128:])  # reg [127 : 0] old_block, shiftrows_block, mixcolumns_block;


      shiftrows_block = Signal(intbv()[128:])
      mixcolumns_block = Signal(intbv()[128:])
      addkey_init_block = Signal(intbv()[128:])  # reg [127 : 0] addkey_init_block, addkey_main_block, addkey_final_block;
      addkey_main_block = Signal(intbv()[128:])  # reg [127 : 0] addkey_block;
      addkey_final_block = Signal(intbv()[128:])  # reg [127 : 0] addkey_block;


      block_new.next[:]   = 0
      muxed_sboxw.next[:] = 0
      block_w0_we.next = 0
      block_w1_we.next = 0
      block_w2_we.next = 0
      block_w3_we.next = 0

      old_b.next[127:92] = block_w0_reg  # old_block            = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};
      old_b.next[91:64] = block_w1_reg
      old_b.next[63:32] = block_w2_reg
      old_b.next[31:00] = block_w3_reg

      shiftrows_block.next[:] = shiftrows(old_b) # shiftrows_block    = shiftrows(old_block);
      mixcolumns_block.next[:] = mixcolumns(shiftrows_block) # mixcolumns_block   = mixcolumns(shiftrows_block);
      addkey_init_block.next[:] = addroundkey(block, round_key) # addkey_init_block  = addroundkey(block, round_key);
      addkey_main_block.next[:] = addroundkey(mixcolumns_block, round_key) # addkey_main_block  = addroundkey(mixcolumns_block, round_key);
      addkey_final_block.next[:] = addroundkey(shiftrows_block, round_key) # addkey_final_block = addroundkey(shiftrows_block, round_key);

      if (update_type == INIT_UPDATE):
        block_new.next[:] = addkey_init_block # block_new    = addkey_init_block;
        block_w0_we.next = 1 # block_w0_we  = 1'b1;
        block_w1_we.next = 1 # block_w1_we  = 1'b1;
        block_w2_we.next = 1 # block_w2_we  = 1'b1;
        block_w3_we.next = 1 # block_w3_we  = 1'b1;

      if (update_type == SBOX_UPDATE):
          block_new.next[127:92] = new_sboxw  # block_new = {new_sboxw, new_sboxw, new_sboxw, new_sboxw};
          block_new.next[91:64] = new_sboxw
          block_new.next[63:32] = new_sboxw
          block_new.next[31:0] = new_sboxw

          if (sword_ctr_reg == 0):
            muxed_sboxw.next[:] = block_w0_reg
            block_w0_we.next = 1

          if (sword_ctr_reg == 1):
            muxed_sboxw.next[:] = block_w1_reg
            block_w1_we.next = 1

          if (sword_ctr_reg == 2):
            muxed_sboxw.next[:] = block_w2_reg
            block_w2_we.next = 1

          if (sword_ctr_reg == 3):
            muxed_sboxw.next[:] = block_w3_reg
            block_w3_we.next = 1

      if (update_type == MAIN_UPDATE):
          block_new.next[:] = addkey_main_block
          block_w0_we.next = 1
          block_w1_we.next = 1
          block_w2_we.next = 1
          block_w3_we.next = 1

      if (update_type == FINAL_UPDATE):
        block_new.next[:] = addkey_final_block
        block_w0_we.next = 1
        block_w1_we.next = 1
        block_w2_we.next = 1
        block_w3_we.next = 1


    # //----------------------------------------------------------------
    # // sword_ctr
    # //
    # // The subbytes word counter with reset and increase logic.
    # //----------------------------------------------------------------


    @always(sword_ctr_rst, sword_ctr_inc)
    def sword_ctr():
      sword_ctr_new.next = 0
      sword_ctr_we.next = 0

      if (sword_ctr_rst):
        sword_ctr_new.next = 0
        sword_ctr_we.next = 1
      elif (sword_ctr_inc):
        sword_ctr_new.next = sword_ctr_reg + 1
        sword_ctr_we.next = 1


    # //----------------------------------------------------------------
    # // round_ctr
    # //
    # // The round counter with reset and increase logic.
    # //----------------------------------------------------------------



    @always(round_ctr_rst, round_ctr_inc, keylen)
    def round_ctr():
        round_ctr_new = intbv(0, min = 0, max = 64)
        round_ctr_we = 0

        if (round_ctr_rst):
            round_ctr_new.next = 0
            round_ctr_we.next = 1
        elif (round_ctr_inc):
          round_ctr_new.next = round_ctr_reg + 1
          round_ctr_we.next = 1



    # //----------------------------------------------------------------
    # // encipher_ctrl
    # //
    # // The FSM that controls the encipher operations.
    # //----------------------------------------------------------------


    @always(enc_ctrl_reg, next)
    def encipher_ctrl():

        num_rounds = Signal(intbv()[4:]) #   reg [3 : 0] num_rounds;

        # // Default assignments.
        sword_ctr_inc.next = 0
        sword_ctr_rst.next = 0
        round_ctr_inc.next = 0
        round_ctr_rst.next = 0
        ready_new.next = 0
        ready_we.next = 0
        update_type.next[:] = NO_UPDATE
        enc_ctrl_new.next[:] = CTRL_IDLE
        enc_ctrl_we.next = 0

        if (keylen == AES_256_BIT_KEY):
          num_rounds.next[:] = AES256_ROUNDS
        else:
          num_rounds.next[:] = AES128_ROUNDS


        if (enc_ctrl_reg == CTRL_IDLE):
          if (next):
            round_ctr_rst.next = 1
            ready_new.next = 0
            ready_we.next = 1
            enc_ctrl_new.next[:] = CTRL_INIT
            enc_ctrl_we.next = 1

        if (enc_ctrl_reg == CTRL_INIT):
          sword_ctr_rst.next = 1
          round_ctr_inc.next = 1
          update_type.next[:] = INIT_UPDATE
          enc_ctrl_new.next[:] = CTRL_SBOX
          enc_ctrl_we.next = 1

        if (enc_ctrl_reg == CTRL_SBOX):
          sword_ctr_inc.next = 1
          update_type.next[:] = SBOX_UPDATE
          if (sword_ctr_reg == 0x03):
            enc_ctrl_new.next[:] = CTRL_MAIN
            enc_ctrl_we.next = 1

        if (enc_ctrl_reg == CTRL_MAIN):
          sword_ctr_rst.next = 1
          round_ctr_inc.next = 1

          if (round_ctr_reg < num_rounds):
            update_type.next[:] = MAIN_UPDATE
            enc_ctrl_new.next[:] = CTRL_SBOX
            enc_ctrl_we.next = 1
          else:
            update_type.next[:] = FINAL_UPDATE
            ready_new.next = 1
            ready_we.next = 1
            enc_ctrl_new.next[:] = CTRL_IDLE
            enc_ctrl_we.next = 1

    return logic, reg_update, sword_ctr, round_ctr
    #return logic, reg_update, sword_ctr, round_ctr, encipher_ctrl, round_logic

# //======================================================================
# // EOF aes_encipher_block.v
# //======================================================================
