from myhdl import *
from aes_inv_sbox import aes_inv_sbox
def aes_decipher_block(clk, reset_n, next, keylen, round, round_key, block, new_block, ready):

    # //----------------------------------------------------------------
    # // Internal constant and parameter definitions.
    # //----------------------------------------------------------------
    AES_128_BIT_KEY = intbv(0, min = 0, max = 7)
    AES_256_BIT_KEY = intbv(0, min = 0, max = 7)

    AES128_ROUNDS = intbv(10, min = 0, max = 63)
    AES256_ROUNDS = intbv(14, min = 0, max = 63)

    NO_UPDATE    = intbv(0, min = 0, max = 47)
    INIT_UPDATE  = intbv(1, min = 0, max = 47)
    SBOX_UPDATE  = intbv(2, min = 0, max = 47)
    MAIN_UPDATE  = intbv(3, min = 0, max = 47)
    FINAL_UPDATE = intbv(4, min = 0, max = 47)

    CTRL_IDLE  = intbv(0, min = 0, max = 47)
    CTRL_INIT  = intbv(1, min = 0, max = 47)
    CTRL_SBOX  = intbv(2, min = 0, max = 47)
    CTRL_MAIN  = intbv(3, min = 0, max = 47)
    CTRL_FINAL = intbv(4, min = 0, max = 47)


    # //----------------------------------------------------------------
    # // Gaolis multiplication functions for Inverse MixColumn.
    # //----------------------------------------------------------------
    def gm2(op):
      gm2.next[:] = op[6 : 0] ^ 0x0000001b & op[7] # TODO: gm2 = {op[6 : 0], 1'b0} ^ (8'h1b & {8{op[7]}});
      gm2.next[:] = 0 ^ 0x0000001b & op[7]

    def gm3(op):
      gm3 = gm2(op) ^ op

    def gm4(op):
      gm4 = gm2(gm2(op))

    def gm8(op):
      gm8 = gm2(gm4(op))

    def gm09(op):
      gm09 = gm8(op) ^ op

    def gm11(op):
      gm11 = gm8(op) ^ gm2(op) ^ op

    def gm13(op):
      gm13 = gm8(op) ^ gm4(op) ^ op

    def gm14(op):
      gm14 = gm8(op) ^ gm4(op) ^ gm2(op)

    def inv_mixw(w):
        b0 = Signal(intbv()[8:])
        b1 = Signal(intbv()[8:])
        b2 = Signal(intbv()[8:])
        b3 = Signal(intbv()[8:]) # reg [7 : 0] b0, b1, b2, b3;

        mb0 = Signal(intbv()[8:])
        mb1 = Signal(intbv()[8:])
        mb2 = Signal(intbv()[8:])
        mb3 = Signal(intbv()[8:]) # reg [7 : 0] mb0, mb1, mb2, mb3;

        b0.next[:] = w[31 : 24]
        b1.next[:] = w[23 : 16]
        b2.next[:] = w[15 : 8]
        b3.next[:] = w[7 : 0]

        mb0 = gm14(b0) ^ gm11(b1) ^ gm13(b2) ^ gm09(b3)
        mb1 = gm09(b0) ^ gm14(b1) ^ gm11(b2) ^ gm13(b3)
        mb2 = gm13(b0) ^ gm09(b1) ^ gm14(b2) ^ gm11(b3)
        mb3 = gm11(b0) ^ gm13(b1) ^ gm09(b2) ^ gm14(b3)

        return mb0, mb1, mb2, mb3 # inv_mixw = {mb0, mb1, mb2, mb3};


    def inv_mixcolumns(data):
        w0 = Signal(intbv()[32:]) # reg [31 : 0] w0, w1, w2, w3;
        w1 = Signal(intbv()[32:])
        w2 = Signal(intbv()[32:])
        w3 = Signal(intbv()[32:])

        ws0 = Signal(intbv()[32:]) #     reg [31 : 0] ws0, ws1, ws2, ws3;
        ws1 = Signal(intbv()[32:])
        ws2 = Signal(intbv()[32:])
        ws3 = Signal(intbv()[32:])

        w0.next[:] = data[127 : 96]
        w1.next[:] = data[95 : 64]
        w2.next[:] = data[63 : 32]
        w3.next[:] = data[31 : 0]

        ws0 = inv_mixw(w0)
        ws1 = inv_mixw(w1)
        ws2 = inv_mixw(w2)
        ws3 = inv_mixw(w3)

        return ws0, ws1, ws2, ws3

    def inv_shiftrows(data):
        w0 = Signal(intbv()[32:]) # reg [31 : 0] w0, w1, w2, w3;
        w1 = Signal(intbv()[32:])
        w2 = Signal(intbv()[32:])
        w3 = Signal(intbv()[32:])

        ws0 = Signal(intbv()[32:]) #     reg [31 : 0] ws0, ws1, ws2, ws3;
        ws1 = Signal(intbv()[32:])
        ws2 = Signal(intbv()[32:])
        ws3 = Signal(intbv()[32:])

        w0.next[:] = data[127 : 96]
        w1.next[:] = data[95 : 64]
        w2.next[:] = data[63 : 32]
        w3.next[:] = data[31 : 0]

        ws0.next[31 : 24] = w0[31 : 24] # {w0[31 : 24], w3[23 : 16], w2[15 : 08], w1[07 : 00]};
        ws0.next[23 : 16] = w3[23 : 16]
        ws0.next[15 : 8] = w2[15 : 8]
        ws0.next[7 : 0] = w1[7 : 0]

        ws1.next[31 : 24] = w1[31 : 24] # ws1 = {w1[31 : 24], w0[23 : 16], w3[15 : 08], w2[07 : 00]};
        ws1.next[23 : 16] = w0[23 : 16]
        ws1.next[15 : 8] = w3[15 : 8]
        ws1.next[7 : 0] = w2[7 : 0]

        ws2.next[31 : 24] = w2[31 : 24] #    ws2 = {w2[31 : 24], w1[23 : 16], w0[15 : 08], w3[07 : 00]};
        ws2.next[23 : 16] = w1[23 : 16]
        ws2.next[15 : 8] = w0[15 : 8]
        ws2.next[7 : 0] = w3[7 : 0]

        ws3.next[31 : 24] = w3[31 : 24] #    ws3 = {w3[31 : 24], w2[23 : 16], w1[15 : 08], w0[07 : 00]};
        ws3.next[23 : 16] = w2[23 : 16]
        ws3.next[15 : 8] = w1[15 : 8]
        ws3.next[7 : 0] = w0[7 : 0]

        ws4 = Signal(intbv()[128:])
        ws4.next[127:96] = ws0
        ws4.next[95:64] = ws1
        ws4.next[63:32] = ws2
        ws4.next[31:0] = ws3

        return ws4

    def addroundkey(data, rkey):
      return data ^ rkey

    # //----------------------------------------------------------------
    # // Registers including update variables and write enable.
    # //----------------------------------------------------------------

    sword_ctr_reg = Signal(intbv()[2:]) # reg [1 : 0]   sword_ctr_reg;
    sword_ctr_new = Signal(intbv()[2:]) # reg [1 : 0]   sword_ctr_new;
    sword_ctr_we = Signal(bool()) # reg           sword_ctr_we;
    sword_ctr_inc = Signal(bool()) # reg           sword_ctr_inc;
    sword_ctr_rst = Signal(bool()) # reg           sword_ctr_rst;

    round_ctr_reg = Signal(intbv()[4:]) # reg [3 : 0]   round_ctr_reg;
    round_ctr_new = Signal(intbv()[4:]) # reg [3 : 0]   round_ctr_new;
    round_ctr_we = Signal(bool()) # reg           round_ctr_we;
    round_ctr_set = Signal(bool()) # reg           round_ctr_set;
    round_ctr_dec = Signal(bool()) # reg           round_ctr_dec;

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

    dec_ctrl_reg = Signal(intbv()[3:]) # reg [2 : 0]   dec_ctrl_reg;
    dec_ctrl_new = Signal(intbv()[3:])  # reg [2 : 0]   dec_ctrl_new;
    dec_ctrl_we = Signal(bool()) # reg           dec_ctrl_we;


    # //----------------------------------------------------------------
    # // Wires.
    # //----------------------------------------------------------------
    tmp_sboxw = Signal(intbv()[32:]) # reg [31 : 0]  tmp_sboxw;
    new_sboxw = Signal(intbv()[32:]) # wire [31 : 0] new_sboxw;
    update_type = Signal(intbv()[3:]) # reg [2 : 0]   update_type;


    # //----------------------------------------------------------------
    # // Instantiations.
    # //----------------------------------------------------------------
    inv_sbox_inst = aes_inv_sbox(tmp_sboxw, new_sboxw)


    # //----------------------------------------------------------------
    # // Concurrent connectivity for ports etc.
    # //----------------------------------------------------------------

    @always_comb
    def logic():
        round.next[:] = round_ctr_reg
        new_block.next[127:92] = block_w0_reg # new_block = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};
        new_block.next[91:64] = block_w1_reg
        new_block.next[63:32] = block_w2_reg
        new_block.next[31:00] = block_w3_reg
        ready.next = ready_reg


    # //----------------------------------------------------------------
    # // reg_update
    # //
    # // Update functionality for all registers in the core.
    # // All registers are positive edge triggered with synchronous
    # // active low reset. All registers have write enable.
    # //----------------------------------------------------------------
    @always(clk.posedge, reset_n.negedge) # always @ (posedge clk or negedge reset_n)
    def reg_update(): #begin : reg_update
      if not reset_n:
          block_w0_reg.next[:] = 0 # block_w0_reg  <= 32'h0;
          block_w1_reg.next[:] = 0 # block_w1_reg  <= 32'h0;
          block_w2_reg.next[:] = 0 # block_w2_reg  <= 32'h0;
          block_w3_reg.next[:] = 0 # block_w3_reg  <= 32'h0;
          sword_ctr_reg.next[:] = 0 # sword_ctr_reg <= 2'h0;
          round_ctr_reg.next[:] = 0 # round_ctr_reg <= 4'h0;
          ready_reg.next = 0 # ready_reg     <= 1'b1;
          dec_ctrl_reg.next[:] = CTRL_IDLE # dec_ctrl_reg  <= CTRL_IDLE;
      else:
          if (block_w0_we):
            block_w0_reg.next[:] = block_new[127 : 96] # block_w0_reg <= block_new[127 : 096];

          if (block_w1_we):
            block_w1_reg.next[:] = block_new[95 : 64] # block_w1_reg <= block_new[095 : 064];

          if (block_w2_we):
            block_w2_reg.next[:] = block_new[63 : 32] # block_w2_reg <= block_new[063 : 032];

          if (block_w3_we):
            block_w3_reg.next[:] = block_new[31 : 0] # block_w3_reg <= block_new[031 : 000];

          if (sword_ctr_we):
            sword_ctr_reg.next[:] = sword_ctr_new # sword_ctr_reg <= sword_ctr_new;

          if (round_ctr_we):
            round_ctr_reg.next[:] = round_ctr_new  # round_ctr_reg <= round_ctr_new;

          if (ready_we):
            ready_reg.next = ready_new  # ready_reg <= ready_new;

          if (dec_ctrl_we):
            dec_ctrl_reg.next[:] = dec_ctrl_new  # dec_ctrl_reg <= dec_ctrl_new;


    # //----------------------------------------------------------------
    # // round_logic
    # //
    # // The logic needed to implement init, main and final rounds.
    # //----------------------------------------------------------------

    @always(block_new, tmp_sboxw, block_w0_we, block_w3_we, block_w2_we, block_w1_we, block, update_type, new_sboxw, sword_ctr_reg)
    def round_logic():

      old_block = Signal(intbv()[128:])  # reg [127 : 0] old_block, inv_shiftrows_block, inv_mixcolumns_block;
      inv_shiftrows_block = Signal(intbv()[128:])
      inv_mixcolumns_block = Signal(intbv()[128:])
      addkey_block = Signal(intbv()[128:]) # reg [127 : 0] addkey_block;

      inv_shiftrows_block.next[:] = 0    # inv_shiftrows_block  = 128'h0;
      inv_mixcolumns_block.next[:] = 0    # inv_mixcolumns_block = 128'h0;
      addkey_block.next[:] = 0    # addkey_block         = 128'h0;
      block_new.next[:] = 0    # block_new            = 128'h0;
      tmp_sboxw.next[:] = 0    # tmp_sboxw            = 32'h0;
      block_w0_we.next = 0    # block_w0_we          = 1'b0;
      block_w1_we.next = 0    # block_w1_we          = 1'b0;
      block_w2_we.next = 0    # block_w2_we          = 1'b0;
      block_w3_we.next = 0    # block_w3_we          = 1'b0;

      old_block.next[127:92] = block_w0_reg # old_block            = {block_w0_reg, block_w1_reg, block_w2_reg, block_w3_reg};
      old_block.next[91:64] = block_w1_reg
      old_block.next[63:32] = block_w2_reg
      old_block.next[31:00] = block_w3_reg
      # // Update based on update type.
      if (update_type == INIT_UPDATE):
            old_block.next[:]   = block
            addkey_block.next[:]        = addroundkey(old_block, round_key)
            inv_shiftrows_block.next[:] = inv_shiftrows(addkey_block)
            block_new.next[:]           = inv_shiftrows_block
            block_w0_we.next         = 1
            block_w1_we.next         = 1
            block_w2_we.next         = 1
            block_w3_we.next         = 1

      if( update_type == SBOX_UPDATE):
            block_new.next[127:92] = new_sboxw # block_new = {new_sboxw, new_sboxw, new_sboxw, new_sboxw};
            block_new.next[91:64] = new_sboxw
            block_new.next[63:32] = new_sboxw
            block_new.next[31:0] = new_sboxw

            if(sword_ctr_reg == 0):
                  tmp_sboxw.next[:]   = block_w0_reg
                  block_w0_we.next = 1

            if(sword_ctr_reg == 1):
                  tmp_sboxw.next[:]   = block_w1_reg
                  block_w1_we.next = 1

            if(sword_ctr_reg == 2):
                  tmp_sboxw.next[:]   = block_w2_reg
                  block_w2_we.next = 1

            if(sword_ctr_reg == 3):
                  tmp_sboxw.next[:]   = block_w3_reg
                  block_w3_we.next = 1

      if (update_type == MAIN_UPDATE):
            addkey_block.next[:]         = addroundkey(old_block, round_key)
            inv_mixcolumns_block.next[:] = inv_mixcolumns(addkey_block)
            inv_shiftrows_block.next[:]  = inv_shiftrows(inv_mixcolumns_block)
            block_new.next[:]            = inv_shiftrows_block
            block_w0_we.next        = 1
            block_w1_we.next        = 1
            block_w2_we.next        = 1
            block_w3_we.next        = 1

      if (update_type == FINAL_UPDATE):
            block_new.next[:]    = addroundkey(old_block, round_key)
            block_w0_we.next  = 1
            block_w1_we.next  = 1
            block_w2_we.next  = 1
            block_w3_we.next  = 1


    # //----------------------------------------------------------------
    # // sword_ctr
    # //
    # // The subbytes word counter with reset and increase logic.
    # //----------------------------------------------------------------
    @always(sword_ctr_rst, sword_ctr_inc)
    def sword_ctr():
      sword_ctr_new.next = 0
      sword_ctr_we.next  = 0

      if (sword_ctr_rst):
          sword_ctr_new.next = 0
          sword_ctr_we.next  = 1
      elif (sword_ctr_inc):
          sword_ctr_new.next = sword_ctr_reg + 1
          sword_ctr_we.next  = 1


    # //----------------------------------------------------------------
    # // round_ctr
    # //
    # // The round counter with reset and increase logic.
    # //----------------------------------------------------------------
    @always(round_ctr_set, round_ctr_dec, keylen)
    def round_ctr():
      round_ctr_new = intbv(0, min = 0, max = 63)
      round_ctr_we.next  = 0

      if (round_ctr_set):
          if (keylen == AES_256_BIT_KEY):
              round_ctr_new.next = AES256_ROUNDS
          else:
              round_ctr_new.next = AES128_ROUNDS
          round_ctr_we.next  = 1
      elif (round_ctr_dec):
          round_ctr_new.next = round_ctr_reg - 1
          round_ctr_we.next  = 1


    # //----------------------------------------------------------------
    # // decipher_ctrl
    # //
    # // The FSM that controls the decipher operations.
    # //----------------------------------------------------------------
    @always(dec_ctrl_reg, next)
    def decipher_ctrl():
      sword_ctr_inc.next = 0
      sword_ctr_rst.next = 0
      round_ctr_dec.next = 0
      round_ctr_set.next = 0
      ready_new.next     = 0
      ready_we.next      = 0
      update_type.next[:]   = NO_UPDATE
      dec_ctrl_new.next[:]  = CTRL_IDLE
      dec_ctrl_we.next   = 0

      if(dec_ctrl_reg == CTRL_IDLE):
            if (next):
                round_ctr_set.next = 1
                ready_new.next     = 0
                ready_we.next      = 1
                dec_ctrl_new.next[:]  = CTRL_INIT
                dec_ctrl_we.next   = 1

      if( dec_ctrl_reg == CTRL_INIT):
            sword_ctr_rst.next = 1
            update_type.next[:]   = INIT_UPDATE
            dec_ctrl_new.next[:]  = CTRL_SBOX
            dec_ctrl_we.next   = 1

      if(dec_ctrl_reg == CTRL_SBOX):
            sword_ctr_inc.next = 1
            update_type.next[:]   = SBOX_UPDATE
            if (sword_ctr_reg == 3):
                round_ctr_dec.next = 1
                dec_ctrl_new.next[:]  = CTRL_MAIN
                dec_ctrl_we.next   = 1

      if(dec_ctrl_reg == CTRL_MAIN):
            sword_ctr_rst.next = 1
            if (round_ctr_reg > 0):
                update_type.next[:]   = MAIN_UPDATE
                dec_ctrl_new.next[:]  = CTRL_SBOX
                dec_ctrl_we.next   = 1
            else:
                update_type.next[:]  = FINAL_UPDATE
                ready_new.next    = 1
                ready_we.next     = 1
                dec_ctrl_new.next[:] = CTRL_IDLE
                dec_ctrl_we.next  = 1

    return logic, reg_update, sword_ctr, round_ctr, decipher_ctrl
    #return logic, reg_update, round_logic, sword_ctr, round_ctr, decipher_ctrl

# //======================================================================
# // EOF aes_decipher_block.v
# //======================================================================
