from myhdl import *

def aes_key_mem(clk, reset_n, key, keylen, init, round, round_key, ready, sboxw, new_sboxw):
# module aes_key_mem(
#                    input wire            clk,
#                    input wire            reset_n,

#                    input wire [255 : 0]  key,
#                    input wire            keylen,
#                    input wire            init,

#                    input wire    [3 : 0] round,
#                    output wire [127 : 0] round_key,
#                    output wire           ready,


#                    output wire [31 : 0]  sboxw,
#                    input wire  [31 : 0]  new_sboxw
#                   );


  # //----------------------------------------------------------------
  # // Parameters.
  # //----------------------------------------------------------------
  # Might have errors.
  AES_128_BIT_KEY = intbv(0, min = 0, max = 7) # localparam AES_128_BIT_KEY = 1'h0;
  AES_256_BIT_KEY = intbv(0, min = 0, max = 7) # localparam AES_256_BIT_KEY = 1'h1;

  AES_128_NUM_ROUNDS = intbv(10, min = 0, max = 63) # localparam AES_128_NUM_ROUNDS = 4'ha;
  AES_256_NUM_ROUNDS = intbv(14, min = 0, max = 63) # localparam AES_256_NUM_ROUNDS = 4'he;

  CTRL_IDLE = intbv(0, min = 0, max = 47) # localparam CTRL_IDLE     = 3'h0;
  CTRL_INIT = intbv(1, min = 0, max = 47) # localparam CTRL_INIT     = 3'h1;
  CTRL_GENERATE = intbv(2, min = 0, max = 47) # localparam CTRL_GENERATE = 3'h2;
  CTRL_DONE = intbv(3, min = 0, max = 47) # localparam CTRL_DONE     = 3'h3;


  # //----------------------------------------------------------------
  # // Registers.
  # //----------------------------------------------------------------
  
  key_mem = [Signal(intbv()[128:]) for n in range(15)]
  key_mem00_new = Signal(intbv()[128:])
  key_mem01_new = Signal(intbv()[128:])
  key_mem02_new = Signal(intbv()[128:])
  key_mem03_new = Signal(intbv()[128:])
  key_mem04_new = Signal(intbv()[128:])
  key_mem05_new = Signal(intbv()[128:])
  key_mem06_new = Signal(intbv()[128:])
  key_mem07_new = Signal(intbv()[128:])
  key_mem08_new = Signal(intbv()[128:])
  key_mem09_new = Signal(intbv()[128:])
  key_mem10_new = Signal(intbv()[128:])
  key_mem11_new = Signal(intbv()[128:])
  key_mem12_new = Signal(intbv()[128:])
  key_mem13_new = Signal(intbv()[128:])
  key_mem14_new = Signal(intbv()[128:])

  key_mem_new = Signal(intbv()[128:]) # reg [127 : 0] key_mem_new;
  key_mem_we = Signal(bool()) #   reg           key_mem_we;

  prev_key0_reg = Signal(intbv()[128:]) #   reg [127 : 0] prev_key0_reg;
  prev_key0_new = Signal(intbv()[128:]) #   reg [127 : 0] prev_key0_new;
  prev_key0_we = Signal(bool()) #   reg           prev_key0_we;

  prev_key1_reg = Signal(intbv(0)[128:]) #   reg [127 : 0] prev_key1_reg;
  prev_key1_new = Signal(intbv()[128:]) #   reg [127 : 0] prev_key1_new;
  prev_key1_we = Signal(bool()) #   reg           prev_key1_we;  
  
  round_ctr_reg = Signal(intbv()[4:]) #  reg [3 : 0] round_ctr_reg;
  round_ctr_new = Signal(intbv()[4:]) #  reg [3 : 0] round_ctr_new;
  round_ctr_rst = Signal(bool()) #   reg         round_ctr_rst;
  round_ctr_inc = Signal(bool()) #   reg         round_ctr_inc;
  round_ctr_we = Signal(bool()) #  reg         round_ctr_we;

  key_mem_ctrl_reg = Signal(intbv()[3:]) #   reg [2 : 0] key_mem_ctrl_reg;
  key_mem_ctrl_new = Signal(intbv()[3:]) #     reg [2 : 0] key_mem_ctrl_new;
  key_mem_ctrl_we = Signal(bool()) #   reg         key_mem_ctrl_we;
  ready_reg = Signal(bool()) #  reg         ready_reg;
  ready_new = Signal(bool()) #  reg         ready_new;
  ready_we = Signal(bool()) #  reg         ready_we;

  rcon_reg = Signal(intbv()[8:]) #   reg [7 : 0] rcon_reg;
  rcon_new = Signal(intbv()[8:]) #  reg [7 : 0] rcon_new;
  rcon_we = Signal(bool()) #   reg         rcon_we;
  rcon_set = Signal(bool()) #   reg         rcon_set;
  rcon_next = Signal(bool()) #   reg         rcon_next;


  # //----------------------------------------------------------------
  # // Wires.
  # //----------------------------------------------------------------
  tmp_sboxw = Signal(intbv()[32:]) #  reg [31 : 0]  tmp_sboxw;
  round_key_update = Signal(bool()) #   reg           round_key_update;
  tmp_round_key = Signal(intbv()[128:]) #   reg [127 : 0] tmp_round_key;


  # //----------------------------------------------------------------
  # // Concurrent assignments for ports.
  # //----------------------------------------------------------------
  @always_comb
  def logic():
    round_key.next[:] = tmp_round_key #  assign round_key = tmp_round_key;
    ready.next = ready_reg #   assign ready     = ready_reg;
    sboxw.next[:] = tmp_sboxw #   assign sboxw     = tmp_sboxw;


  # //----------------------------------------------------------------
  # // reg_update
  # //
  # // Update functionality for all registers in the core.
  # // All registers are positive edge triggered with asynchronous
  # // active low reset. All registers have write enable.
  # //----------------------------------------------------------------
  @always(clk.posedge, reset_n.negedge) # always @ (posedge clk or negedge reset_n)
  def reg_update(): #     begin: reg_update
      if not reset_n:
          for i in range(15):
            key_mem[i].next[:] = 0 #             key_mem[i] <= 128'h0;

          rcon_reg.next[:] = 0 # rcon_reg         <= 8'h0;
          ready_reg.next = 0 # ready_reg        <= 1'b0;
          round_ctr_reg.next[:] = 0 # round_ctr_reg    <= 4'h0;
          key_mem_ctrl_reg.next[:] = CTRL_IDLE # key_mem_ctrl_reg <= CTRL_IDLE;
      else:
          if (round_ctr_we):
            round_ctr_reg.next[:] = round_ctr_new # round_ctr_reg <= round_ctr_new;

          if (ready_we):
            ready_reg.next = ready_new #ready_reg <= ready_new;

          if (rcon_we):
            rcon_reg.next[:] = rcon_new # rcon_reg <= rcon_new;

          if (key_mem_we):
            key_mem[round_ctr_reg] = key_mem_new # key_mem[round_ctr_reg] <= key_mem_new;

          if (prev_key0_we):
            prev_key0_reg = prev_key0_new # prev_key0_reg <= prev_key0_new;

          if (prev_key1_we):
            prev_key1_reg = prev_key1_new # prev_key1_reg <= prev_key1_new;

          if (key_mem_ctrl_we):
            key_mem_ctrl_reg.next[:] = key_mem_ctrl_new # key_mem_ctrl_reg <= key_mem_ctrl_new;
        

  # //----------------------------------------------------------------
  # // key_mem_read
  # //
  # // Combinational read port for the key memory.
  # //----------------------------------------------------------------
  @always(round_ctr_reg, key_mem[0], key_mem[1], key_mem[2], key_mem[3], key_mem[4], key_mem[5], key_mem[6], key_mem[7],
                key_mem[8], key_mem[9], key_mem[10], key_mem[11], key_mem[12], key_mem[13], key_mem[14]) # always @*
  def key_mem_read():
      tmp_round_key.next[:] = key_mem[round_ctr_reg];
    


  # //----------------------------------------------------------------
  # // round_key_gen
  # //
  # // The round key generator logic for AES-128 and AES-256.
  # //----------------------------------------------------------------
  @always(prev_key0_reg, prev_key1_reg, rcon_reg, round_key_update, keylen, round_ctr_reg, key) #  always @*
  def round_key_gen():
      w0  = Signal(intbv()[32:]) #      reg [31 : 0] w0, w1, w2, w3, w4, w5, w6, w7;
      w1  = Signal(intbv()[32:])
      w2  = Signal(intbv()[32:])
      w3  = Signal(intbv()[32:])
      w4  = Signal(intbv()[32:])
      w5  = Signal(intbv()[32:])
      w6  = Signal(intbv()[32:])
      w7  = Signal(intbv()[32:])

      k0  = Signal(intbv()[32:]) #       reg [31 : 0] k0, k1, k2, k3;
      k1  = Signal(intbv()[32:])
      k2  = Signal(intbv()[32:])
      k3  = Signal(intbv()[32:])

      rconw  = Signal(intbv()[32:]) #       reg [31 : 0] rconw, rotstw, tw, trw;
      rotstw  = Signal(intbv()[32:])
      tw  = Signal(intbv()[32:])
      trw  = Signal(intbv()[32:])

      # // Default assignments.
      key_mem_new.next[:] = 0 # key_mem_new   = 128'h0;
      key_mem_we.next = 0 #key_mem_we    = 1'b0;
      prev_key0_new.next[:] = 0 #prev_key0_new = 128'h0;
      prev_key0_we.next = 0 #prev_key0_we  = 1'b0;
      prev_key1_new.next[:] = 0 #prev_key1_new = 128'h0;
      prev_key1_we.next = 0 #prev_key1_we  = 1'b0;

      k0.next[:] = 0 # k0 = 32'h0;
      k1.next[:] = 0 # k1 = 32'h0;
      k2.next[:] = 0 # k2 = 32'h0;
      k3.next[:] = 0 # k3 = 32'h0;

      rcon_set.next   = 1 #rcon_set   = 1'b1;
      rcon_next.next  = 0 # rcon_next  = 1'b0;

      # // Extract words and calculate intermediate values.
      # // Perform rotation of sbox word etc.
      
      w0.next[:] = prev_key0_reg[127 : 96]
      w1.next[:] = prev_key0_reg[95 : 64]
      w2.next[:] = prev_key0_reg[63 : 32]
      w3.next[:] = prev_key0_reg[31 : 0]

      w4.next[:] = prev_key1_reg[127 : 96]
      w5.next[:] = prev_key1_reg[95 : 64]
      w6.next[:] = prev_key1_reg[63 : 32]
      w7.next[:] = prev_key1_reg[31 : 0]


      rconw.next[31 :24] = rcon_reg[7:0] # rconw = {rcon_reg, 24'h0};
      rconw.next[23 :0] = 0 # not sure if should be 23 or 24.
      
      tmp_sboxw.next[:] = w7;
      rotstw.next[31:8] = new_sboxw[23: 00] # rotstw = {new_sboxw[23 : 00], new_sboxw[31 : 24]};
      rotstw.next[7:0] = new_sboxw[31: 24]
      trw.next[:] = rotstw ^ rconw;
      tw.next[:] = new_sboxw;

      # // Generate the specific round keys.

      if (round_key_update):
          rcon_set.next   = 0;
          key_mem_we.next = 1;
          if (keylen == AES_128_BIT_KEY):
              if (round_ctr_reg == 0):
                  key_mem_new.next[:]   = key[255 : 128];
                  prev_key1_new.next[:] = key[255 : 128];
                  prev_key1_we.next  = 1;
                  rcon_next.next     = 1;
              else:
                  k0.next[:] = w4 ^ trw;
                  k1.next[:] = w5 ^ w4 ^ trw;
                  k2.next[:] = w6 ^ w5 ^ w4 ^ trw;
                  k3.next[:] = w7 ^ w6 ^ w5 ^ w4 ^ trw;

                  key_mem_new.next[127:92] = k0 #key_mem_new   = {k0, k1, k2, k3};
                  key_mem_new.next[91:64] = k1
                  key_mem_new.next[63:32] = k2
                  key_mem_new.next[31:0] = k3

                  prev_key1_new.next[127:92] = k0 #prev_key1_new = {k0, k1, k2, k3};
                  prev_key1_new.next[91:64] = k1
                  prev_key1_new.next[63:32] = k2
                  prev_key1_new.next[31:0] = k3

                  
                  prev_key1_we.next  = 1
                  rcon_next.next     = 1

          if (keylen == AES_256_BIT_KEY):
                if (round_ctr_reg == 0):
                  key_mem_new.next[:]   = key[255 : 128] # key_mem_new   = key[255 : 128];
                  prev_key0_new.next[:] = key[255 : 128] # prev_key0_new = key[255 : 128];
                  prev_key0_we.next  = 1; # prev_key0_we  = 1'b1;
                elif (round_ctr_reg == 1):
                  key_mem_new.next[:]   = key[127 : 0] # key_mem_new   = key[127 : 0];
                  prev_key1_new.next[:] = key[127 : 0] #    prev_key1_new = key[127 : 0];
                  prev_key1_we.next  = 1
                  rcon_next.next     = 1
                else:
                    if (round_ctr_reg[0] == 0):
                        k0.next[:] = w0 ^ trw
                        k1.next[:] = w1 ^ w0 ^ trw
                        k2.next[:] = w2 ^ w1 ^ w0 ^ trw
                        k3.next[:] = w3 ^ w2 ^ w1 ^ w0 ^ trw
                    else:
                        k0.next[:] = w0 ^ tw
                        k1.next[:] = w1 ^ w0 ^ tw
                        k2.next[:] = w2 ^ w1 ^ w0 ^ tw
                        k3.next[:] = w3 ^ w2 ^ w1 ^ w0 ^ tw
                        rcon_next.next = 1

                    # // Store the generated round keys.
                    key_mem_new.next[127:92] = k0 # key_mem_new   = {k0, k1, k2, k3};
                    key_mem_new.next[91:64] = k1
                    key_mem_new.next[63:32] = k2
                    key_mem_new.next[31:0] = k3

                    prev_key1_new.next[127:92] = k0 # prev_key1_new = {k0, k1, k2, k3};
                    prev_key1_new.next[91:64] = k1
                    prev_key1_new.next[63:32] = k2
                    prev_key1_new.next[31:0] = k3
                    
                    
                    prev_key1_we.next  = 1
                    prev_key0_new.next[:] = prev_key1_reg;
                    prev_key0_we.next  = 1


  # //----------------------------------------------------------------
  # // rcon_logic
  # //
  # // Caclulates the rcon value for the different key expansion
  # // iterations.
  # //----------------------------------------------------------------
  @always() # always @*   begin : rcon_logic
  def rcon_logic():
      tmp_rcon = Signal(intbv()[8:]) # reg [7 : 0] tmp_rcon;
      rcon_new.next = 0 # rcon_new = 8'h00;
      rcon_we.next  = 0

      tmp_rcon.next[:] = rcon_reg[7:1]  # tmp_rcon = {rcon_reg[6 : 0], 1'b0} ^ (8'h & {8{rcon_reg[7]}});
      tmp_rcon.next[:] = 0  # (8'h1b & {8{rcon_reg[7]}}) # TODO: how to translate this??? and add afterward ^ for the above
      if (rcon_set):
          rcon_new.next = 141 #8d
          rcon_we.next  = 1

      if (rcon_next):
          rcon_new.next = tmp_rcon[7 : 0]
          rcon_we.next  = 1

  # //----------------------------------------------------------------
  # // round_ctr
  # //
  # // The round counter logic with increase and reset.
  # //----------------------------------------------------------------
  @always(round_ctr_rst, round_ctr_inc, round_ctr_reg)#always @*  begin : round_ctr
  def round_ctr(): 
      round_ctr_new.next = 0
      round_ctr_we.next  = 0

      if (round_ctr_rst):
          round_ctr_new.next = 0 # 0x0000
          round_ctr_we.next  = 1

      elif (round_ctr_inc):
          round_ctr_new.next = round_ctr_reg + 1
          round_ctr_we.next  = 1


  # //----------------------------------------------------------------
  # // key_mem_ctrl
  # //
  # //
  # // The FSM that controls the round key generation.
  # //----------------------------------------------------------------
  #always @*   begin: key_mem_ctrl
  @always(keylen, key_mem_ctrl_reg, init, round_ctr_reg)
  def key_mem_ctrl():
      num_rounds = Signal(intbv()[4:]) # reg [3 : 0] num_rounds;

      # // Default assignments.
      ready_new.next        = 0
      ready_we.next         = 0
      round_key_update.next = 0
      round_ctr_rst.next    = 0
      round_ctr_inc.next    = 0
      key_mem_ctrl_new.next[:] = CTRL_IDLE
      key_mem_ctrl_we.next  = 0

      if (keylen == AES_128_BIT_KEY):
        num_rounds.next[:] = AES_128_NUM_ROUNDS # num_rounds = AES_128_NUM_ROUNDS;
      else:
        num_rounds.next[:] = AES_256_NUM_ROUNDS # num_rounds = AES_256_NUM_ROUNDS;

      if (key_mem_ctrl_reg == CTRL_IDLE):
            if (init):
                ready_new.next        = 0
                ready_we.next         = 1
                key_mem_ctrl_new.next[:] = CTRL_INIT
                key_mem_ctrl_we.next  = 1

      if(key_mem_ctrl_reg == CTRL_INIT):
            round_ctr_rst.next    = 1
            key_mem_ctrl_new.next[:] = CTRL_GENERATE;
            key_mem_ctrl_we.next  = 1

      if(key_mem_ctrl_reg == CTRL_GENERATE):
            round_ctr_inc.next    = 1
            round_key_update.next = 1
            if (round_ctr_reg == num_rounds):
                key_mem_ctrl_new.next[:] = CTRL_DONE
                key_mem_ctrl_we.next  = 1

      if(key_mem_ctrl_reg == CTRL_DONE):
            ready_new.next        = 1
            ready_we.next         = 1
            key_mem_ctrl_new.next[:] = CTRL_IDLE
            key_mem_ctrl_we.next  = 1

  return logic, key_mem_read ,reg_update, round_ctr


# //======================================================================
# // EOF aes_key_mem.v
# //======================================================================
