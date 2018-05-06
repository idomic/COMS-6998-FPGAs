
from myhdl import *
from aes_key_mem import aes_key_mem
from aes_encipher_block import aes_encipher_block
from aes_decipher_block import aes_decipher_block
from aes_sbox import aes_sbox

def aes_core(clk, reset_n, encdec, init, next, ready, key, keylen, block, result, result_valid):

  # //----------------------------------------------------------------
  # // Internal constant and parameter definitions.
  # //----------------------------------------------------------------
  CTRL_IDLE  = intbv(0, min = 0, max = 31) # is it like that? 2h0 == 0
  CTRL_INIT  = intbv(1, min = 0, max = 31)
  CTRL_NEXT  = intbv(2, min = 0, max = 31)


  # //----------------------------------------------------------------
  # // Registers including update variables and write enable.
  # //----------------------------------------------------------------
  aes_core_ctrl_reg = Signal(intbv()[2:]) # reg [1 : 0] aes_core_ctrl_reg;
  aes_core_ctrl_new = Signal(intbv()[2:])# reg [1 : 0] aes_core_ctrl_new;
  aes_core_ctrl_we = Signal(bool()) # reg         aes_core_ctrl_we;

  result_valid_reg = Signal(bool()) # reg         result_valid_reg;
  result_valid_new = Signal(bool()) # reg         result_valid_new;
  result_valid_we = Signal(bool()) # reg         result_valid_we;

  ready_reg = Signal(bool()) # reg         ready_reg;
  ready_new = Signal(bool()) # reg         ready_new;
  ready_we = Signal(bool())# reg         ready_we;


  # //----------------------------------------------------------------
  # // Wires.
  # //----------------------------------------------------------------


  #init_state = Signal(bool()) # reg            init_state;
  round_key = Signal(intbv()[128:])# wire [127 : 0] round_key;
  key_ready = Signal(bool()) # wire           key_ready;
  state_init = Signal(bool())
  enc_next = Signal(bool()) #   reg            enc_next;
  enc_round_nr = Signal(intbv()[4:]) #  wire [3 : 0]   enc_round_nr;
  enc_new_block = Signal(intbv()[128:]) #  wire [127 : 0] enc_new_block;
  enc_ready = Signal(bool()) #  wire           enc_ready;
  enc_sboxw = Signal(intbv()[32:]) #wire [31 : 0]  enc_sboxw;

  dec_next = Signal(bool()) # reg            dec_next;
  dec_round_nr = Signal(intbv()[4:]) #  wire [3 : 0]   dec_round_nr;
  dec_new_block = Signal(intbv()[128:]) # wire [127 : 0] dec_new_block;
  dec_ready = Signal(bool()) # wire           dec_ready;

  muxed_new_block = Signal(intbv()[128:]) # reg [127 : 0]  muxed_new_block;
  muxed_round_nr = Signal(intbv()[4:]) # reg [3 : 0]    muxed_round_nr;
  muxed_ready = Signal(bool()) # reg            muxed_ready;

  keymem_sboxw = Signal(intbv()[32:]) # wire [31 : 0]  keymem_sboxw;

  muxed_sboxw = Signal(intbv()[32:]) # reg [31 : 0]   muxed_sboxw;
  new_sboxw = Signal(intbv()[32:]) #  wire [31 : 0]  new_sboxw;


  # //----------------------------------------------------------------
  # // Instantiations.
  # //----------------------------------------------------------------

  enc_block = aes_encipher_block(clk, reset_n, enc_next, keylen, enc_round_nr, round_key, enc_sboxw, new_sboxw, block, enc_new_block, enc_ready)
  dec_block = aes_decipher_block(clk, reset_n, dec_next, keylen, dec_round_nr, round_key, block, dec_new_block, dec_ready)
  keymem = aes_key_mem(clk, reset_n, key, keylen, init, muxed_round_nr, round_key, key_ready, keymem_sboxw, new_sboxw)
  sbox = aes_sbox(muxed_sboxw, new_sboxw)

  # //----------------------------------------------------------------
  # // Concurrent connectivity for ports etc.
  # //----------------------------------------------------------------
  @always_comb
  def logic():
    ready.next = ready_reg  # assign ready        = ready_reg;
    result.next[:] = muxed_new_block  # assign result       = muxed_new_block;
    result_valid.next = result_valid_reg  # assign result_valid = result_valid_reg;


  # //----------------------------------------------------------------
  # // reg_update
  # //
  # // Update functionality for all registers in the core.
  # // All registers are positive edge triggered with asynchronous
  # // active low reset. All registers have write enable.
  # //----------------------------------------------------------------
  @always(clk.posedge, reset_n.negedge)
  def reg_update():
      if not reset_n:
          result_valid_reg.next  = 0
          ready_reg.next         = 1
          aes_core_ctrl_reg.next[:] = CTRL_IDLE
      else:
          if (result_valid_we):
            result_valid_reg.next = result_valid_new

          if (ready_we):
            ready_reg.next = ready_new

          if (aes_core_ctrl_we):
            aes_core_ctrl_reg.next[:] = aes_core_ctrl_new

  # //----------------------------------------------------------------
  # // sbox_mux
  # //
  # // Controls which of the encipher datapath or the key memory
  # // that gets access to the sbox.
  # //----------------------------------------------------------------
  @always(state_init, keymem_sboxw, enc_sboxw)
  def sbox_mux():
      if (state_init):
          muxed_sboxw.next[:] = keymem_sboxw
      else:
          muxed_sboxw.next[:] = enc_sboxw


  # //----------------------------------------------------------------
  # // encdex_mux
  # //
  # // Controls which of the datapaths that get the next signal, have
  # // access to the memory as well as the block processing result.
  # //----------------------------------------------------------------
  @always(encdec, next, enc_round_nr, enc_new_block, enc_ready)
  def encdec_mux():
      enc_next.next = 0
      dec_next.next = 0

      if (encdec):
          # // Encipher operations
          enc_next.next        = next
          muxed_round_nr.next[:]  = enc_round_nr
          muxed_new_block.next[:] = enc_new_block
          muxed_ready.next     = enc_ready
      else:
          # // Decipher operations
          dec_next.next        = next
          muxed_round_nr.next[:]  = dec_round_nr
          muxed_new_block.next[:] = dec_new_block
          muxed_ready.next     = dec_ready


  # //----------------------------------------------------------------
  # // aes_core_ctrl
  # //
  # // Control FSM for aes core. Basically tracks if we are in
  # // key init, encipher or decipher modes and connects the
  # // different submodules to shared resources and interface ports.
  # //----------------------------------------------------------------
  @always(init, next, key_ready, muxed_ready)
  def aes_core_ctrl():
      state_init = Signal(bool()) # TODO: maybe can cause error
      state_init.next        = 0
      ready_new.next         = 0
      ready_we.next          = 0
      result_valid_new.next  = 0
      result_valid_we.next   = 0
      aes_core_ctrl_new.next[:] = CTRL_IDLE
      aes_core_ctrl_we.next  = 0

      if (aes_core_ctrl_reg == CTRL_IDLE):
            if (init):
                state_init.next        = 1
                ready_new.next         = 0
                ready_we.next          = 1
                result_valid_new.next  = 0
                result_valid_we.next   = 1
                aes_core_ctrl_new.next[:] = CTRL_INIT
                aes_core_ctrl_we.next  = 1
            elif (next):
                state_init.next        = 0
                ready_new.next         = 0
                ready_we.next          = 1
                result_valid_new.next  = 0
                result_valid_we.next   = 1
                aes_core_ctrl_new.next[:] = CTRL_NEXT
                aes_core_ctrl_we.next  = 1

      if(aes_core_ctrl_reg == CTRL_INIT):
            state_init.next = 1
            if (key_ready):
                ready_new.next         = 1
                ready_we.next          = 1
                aes_core_ctrl_new.next[:] = CTRL_IDLE
                aes_core_ctrl_we.next  = 1

      if(aes_core_ctrl_reg == CTRL_NEXT):
            state_init = 0
            if (muxed_ready):
                ready_new.next         = 1
                ready_we.next          = 1
                result_valid_new.next  = 1
                result_valid_we.next   = 1
                aes_core_ctrl_new.next[:] = CTRL_IDLE
                aes_core_ctrl_we.next  = 1

  return enc_block, dec_block, keymem, logic, reg_update, sbox_mux , encdec_mux



# //======================================================================
# // EOF aes_core.v
# //======================================================================
