from myhdl import *
from aes_core import aes_core

def aes(clk, reset_n, cs, we, address, write_data, read_data):
           

  # //----------------------------------------------------------------
  # // Internal constant and parameter definitions.
  # //----------------------------------------------------------------

  ADDR_NAME0       = intbv(0, min = 0, max = 255)  #intbv(0)[8:] # 8'h00;
  ADDR_NAME1       = intbv(1, min = 0, max = 255)  #intbv(1)[8:] # 8'h01;
  ADDR_VERSION     = intbv(2, min = 0, max = 255)  #intbv(2)[8:] # 8'h02;

  ADDR_CTRL        = intbv(8, min = 0, max = 255)  #intbv(8)[8:] # 8'h08;
  CTRL_INIT_BIT    = bool(0)
  CTRL_NEXT_BIT    = bool(1)

  ADDR_STATUS      = intbv(9, min = 0, max = 255)  #intbv(9)[8:] # 8'h09;
  STATUS_READY_BIT = bool(0)
  STATUS_VALID_BIT = bool(1)

  ADDR_CONFIG      = address
  CTRL_ENCDEC_BIT  = bool(0)
  CTRL_KEYLEN_BIT  = bool(1)

  ADDR_KEY0        = intbv(16, min = 0, max = 255) # 8'h10;
  ADDR_KEY7        = intbv(23, min = 0, max = 255) # 8'h17;

  ADDR_BLOCK0      = intbv(32, min = 0, max = 255) # 8'h20;
  ADDR_BLOCK3      = intbv(35, min = 0, max = 255) # 8'h23;

  ADDR_RESULT0     = intbv(48, min = 0, max = 255) # 8'h30;
  ADDR_RESULT3     = intbv(51, min = 0, max = 255) # 8'h33;

  CORE_NAME0       = 0x61657320 #// "aes "
  CORE_NAME1       = 0x20202020 #; // "    "
  CORE_VERSION     = 0x302e3630 #; // "0.60"


  # //----------------------------------------------------------------
  # // Registers including update variables and write enable.
  # //----------------------------------------------------------------
  
  init_reg = Signal(bool()) #reg init_reg;
  init_new = Signal(bool()) #reg init_new;
  next_reg = Signal(bool()) # reg next_reg;
  next_new = Signal(bool()) # reg next_new;
  encdec_reg = Signal(bool()) #reg encdec_reg;
  keylen_reg = Signal(bool()) #reg keylen_reg;
  config_we = Signal(bool()) #reg config_we;

  block_reg = [Signal(intbv()[32:]) for n in range(4)] # reg [31 : 0] block_reg [0 : 3];
  block_we  = Signal(bool()) # reg          block_we;

  key_reg = [Signal(intbv()[32:]) for n in range(8)] # reg [31 : 0] key_reg [0 : 7];
  key_we  = Signal(bool()) # reg          key_we;
  
  result_reg = Signal(intbv()[128:]) # reg [127 : 0] result_reg;
  valid_reg = Signal(bool()) # reg           valid_reg;
  ready_reg = Signal(bool()) # reg           ready_reg;
  
  


  # //----------------------------------------------------------------
  # // Wires.
  # //----------------------------------------------------------------

  tmp_read_data = Signal(intbv()[32:]) # reg [31 : 0]   tmp_read_data;
  core_encdec = Signal(bool()) # wire           core_encdec;
  core_init = Signal(bool()) #  wire           core_init;
  core_next = Signal(bool()) #  wire           core_next;
  core_ready = Signal(bool()) #  wire           core_ready;
  core_key = Signal(intbv()[256:]) # wire [255 : 0] core_key;
  core_keylen = Signal(bool()) #  wire           core_keylen;
  core_block = Signal(intbv()[128:]) # wire [127 : 0] core_block;
  core_result = Signal(intbv()[128:]) # wire [127 : 0] core_result;
  core_valid = Signal(bool()) #  wire           core_valid;


  # //----------------------------------------------------------------
  # // Concurrent connectivity for ports etc.
  # //----------------------------------------------------------------
  @always_comb
  def logic():
    read_data.next[:] = tmp_read_data #assign read_data = tmp_read_data;

    core_key.next[256:224] = key_reg[0]
    core_key.next[224:192] = key_reg[1]
    core_key.next[192:160] = key_reg[2]
    core_key.next[160:128] = key_reg[3]
    core_key.next[128: 96] = key_reg[4]
    core_key.next[96 : 64] = key_reg[5]
    core_key.next[64 : 32] = key_reg[6]
    core_key.next[32 :  0] = key_reg[7] #  assign core_key = {key_reg[0], key_reg[1], key_reg[2], key_reg[3],
                                                              #key_reg[4], key_reg[5], key_reg[6], key_reg[7]};
    core_block.next[128: 96] = block_reg[0]
    core_block.next[96 : 64] = block_reg[1]
    core_block.next[64 : 32] = block_reg[2]
    core_block.next[32 :  0] = block_reg[3]  #  assign core_block  = {block_reg[0], block_reg[1],
                                              #                       block_reg[2], block_reg[3]};
    core_init.next = init_reg #  assign core_init   = init_reg;
    core_next.next = next_reg # assign core_next   = next_reg;
    core_encdec.next = encdec_reg # assign core_encdec = encdec_reg;
    core_keylen.next = keylen_reg # assign core_keylen = keylen_reg;


  # //----------------------------------------------------------------
  # // core instantiation.
  # //----------------------------------------------------------------
  core = aes_core(clk, reset_n, core_encdec, core_init, core_next, core_ready, core_key, core_keylen, core_block, core_result, core_valid)


  # //----------------------------------------------------------------
  # // reg_update
  # // Update functionality for all registers in the core.
  # // All registers are positive edge triggered with asynchronous
  # // active low reset.
  # //----------------------------------------------------------------
  @always(clk.posedge, reset_n.negedge) # always @ (posedge clk or negedge reset_n) begin : reg_update
  def reg_update():
      # integer i;

      if not reset_n: # if (!reset_n)
          for i in range(4): #        for (i = 0 ; i < 4 ; i = i + 1)
            block_reg[i].next[:] = 0 #            block_reg[i] <= 32'h0;

          for i in range(8): # for (i = 0 ; i < 8 ; i = i + 1)
            key_reg[i].next[:] = 0 # key_reg[i] <= 32'h0;

          init_reg.next = 0 # init_reg   <= 1'b0;
          next_reg.next = 0 # next_reg   <= 1'b0;
          encdec_reg.next = 0 #          encdec_reg <= 1'b0;
          keylen_reg.next = 0 # keylen_reg <= 1'b0;

          result_reg.next[:] = 0 # result_reg <= 128'h0; might have an error
          valid_reg.next = 0 # valid_reg  <= 1'b0;
          ready_reg.next = 0 # ready_reg  <= 1'b0;
      else:
          ready_reg.next = core_ready #          ready_reg  <= core_ready;
          valid_reg.next = core_valid # valid_reg  <= core_valid;
          result_reg.next = core_result # result_reg <= core_result;
          init_reg.next = init_new # init_reg   <= init_new;
          next_reg.next = next_new # next_reg   <= next_new;

          if config_we:
              encdec_reg.next = write_data[CTRL_ENCDEC_BIT]
              keylen_reg.next = write_data[CTRL_KEYLEN_BIT]

          if key_we:
            key_reg[address[2:0]].next[:] = write_data #       key_reg[address[2 : 0]] <= write_data;

          if block_we:
            block_reg[address[1:0]].next[:] = write_data #             block_reg[address[1 : 0]] <= write_data;


  # //----------------------------------------------------------------
  # // api
  # //
  # // The interface command decoding logic.
  # //----------------------------------------------------------------
  # always @*
  #   begin : api
  #     init_new      = 1'b0;
  #     next_new      = 1'b0;
  #     config_we     = 1'b0;
  #     key_we        = 1'b0;
  #     block_we      = 1'b0;
  #     tmp_read_data = 32'h0;


  @always(address, cs, we, write_data, key_reg[0], key_reg[1], key_reg[2], key_reg[3], key_reg[4], key_reg[5], key_reg[6], key_reg[7], block_reg[0], block_reg[1], block_reg[2], block_reg[3], keylen_reg, encdec_reg, next_reg, init_reg, result_reg, valid_reg, ready_reg)
  def api():
      init_new.next = 0 #     init_new      = 1'b0;
      next_new.next = 0 #     next_new      = 1'b0;
      config_we.next = 0    #     config_we     = 1'b0;
      key_we.next = 0 #     key_we        = 1'b0;
      block_we.next  = 0#     block_we      = 1'b0;
      tmp_read_data.next[:]  = 0#     tmp_read_data = 32'h0;

      if cs:
        if we:
          if (address == ADDR_CTRL):
              init_new.next = write_data[CTRL_INIT_BIT]; # init_new = write_data[CTRL_INIT_BIT];
              next_new.next = write_data[CTRL_NEXT_BIT]; # next_new = write_data[CTRL_NEXT_BIT];

          if (address == ADDR_CONFIG):
            config_we.next = 1 # config_we = 1'b1;

          if ((address >= ADDR_KEY0) and (address <= ADDR_KEY7)):
            key_we.next = 1 # key_we = 1'b1;

          if ((address >= ADDR_BLOCK0) and (address <= ADDR_BLOCK3)):
            block_we.next = 1 # block_we = 1'b1;

      else:
          if(address):
            if (address == ADDR_NAME0):
              tmp_read_data.next[:] = CORE_NAME0 # tmp_read_data = CORE_NAME0;
            elif address == ADDR_NAME1:
              tmp_read_data.next[:] = CORE_NAME1 # tmp_read_data = CORE_NAME1;
            elif address == ADDR_VERSION:
              tmp_read_data.next[:] = CORE_VERSION # tmp_read_data = CORE_VERSION;
            elif address == ADDR_CTRL:  # tmp_read_data = {28'h0, keylen_reg, encdec_reg, next_reg, init_reg};
              tmp_read_data.next[32:4] = 0
              tmp_read_data.next[4 :3] = keylen_reg
              tmp_read_data.next[3 :2] = encdec_reg
              tmp_read_data.next[2 :1] = next_reg
              tmp_read_data.next[1 :0] = init_reg
            elif address == ADDR_STATUS: # tmp_read_data = {30'h0, valid_reg, ready_reg};
              tmp_read_data.next[32:2] = 0
              tmp_read_data.next[2 :1] = valid_reg
              tmp_read_data.next[1 :0] = ready_reg

          if ((address >= ADDR_RESULT0) and (address <= ADDR_RESULT3)):
            if (address == 48):
                tmp_read_data.next[:] = result_reg[128: 96]
            if (address == 49):
                tmp_read_data.next[:] = result_reg[96 : 64]
            if (address == 50):
                tmp_read_data.next[:] = result_reg[64 : 32]
            if (address == 51):
                tmp_read_data.next[:] = result_reg[32 :  0]
              #tmp_read_data.next[:] = result_reg[(3 - (address - ADDR_RESULT0)) * 32 +: 32]
              #tmp_read_data = result_reg[(3 - (address - ADDR_RESULT0)) * 32 +: 32];
  return core, api, reg_update, logic

# //======================================================================
# // EOF aes.v
# //======================================================================
