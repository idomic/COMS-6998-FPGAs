from myhdl import *

def aes_inv_sbox(sword, new_sword):


  # //----------------------------------------------------------------
  # // The inverse sbox array.
  # //----------------------------------------------------------------
  inv_sbox = [Signal(intbv()[8:]) for n in range(256)] # wire [7 : 0] inv_sbox [0 : 255];


  # //----------------------------------------------------------------
  # // Four parallel muxes.
  # //----------------------------------------------------------------

  new_sword.next[31:24] = inv_sbox[sword[31:24]] #  assign new_sword[31 : 24] = inv_sbox[sword[31 : 24]];
  new_sword.next[23:16] = inv_sbox[sword[23:16]] # assign new_sword[23:16] = inv_sbox[sword[23 : 16]];
  new_sword.next[15:8] = inv_sbox[sword[15:8]] # assign new_sword[15 : 08] = inv_sbox[sword[15 : 08]];
  new_sword.next[7:0] = inv_sbox[sword[7:0]] # assign new_sword[07 : 00] = inv_sbox[sword[07 : 00]];

  #(intbv.*)
  # //----------------------------------------------------------------
  # // Creating the contents of the array.
  # //----------------------------------------------------------------
  inv_sbox[0x00000000] = Signal(intbv(0x00000052)) # assign inv_sbox[8'h00] = 8'h52;
  inv_sbox[0x00000001] = Signal(intbv(0x00000009))
  inv_sbox[0x00000002] = Signal(intbv(0x0000006a))
  inv_sbox[0x00000003] = Signal(intbv(0x000000d5))
  inv_sbox[0x00000004] = Signal(intbv(0x00000030))
  inv_sbox[0x00000005] = Signal(intbv(0x00000036))
  inv_sbox[0x00000006] = Signal(intbv(0x000000a5))
  inv_sbox[0x00000007] = Signal(intbv(0x00000038))
  inv_sbox[0x00000008] = Signal(intbv(0x000000bf))
  inv_sbox[0x00000009] = Signal(intbv(0x00000040))
  inv_sbox[0x0000000a] = Signal(intbv(0x000000a3))
  inv_sbox[0x0000000b] = Signal(intbv(0x0000009e))
  inv_sbox[0x0000000c] = Signal(intbv(0x00000081))
  inv_sbox[0x0000000d] = Signal(intbv(0x000000f3))
  inv_sbox[0x0000000e] = Signal(intbv(0x000000d7))
  inv_sbox[0x0000000f] = Signal(intbv(0x000000fb))
  inv_sbox[0x00000010] = Signal(intbv(0x0000007c))
  inv_sbox[0x00000011] = Signal(intbv(0x000000e3))
  inv_sbox[0x00000012] = Signal(intbv(0x00000039))
  inv_sbox[0x00000013] = Signal(intbv(0x00000082))
  inv_sbox[0x00000014] = Signal(intbv(0x0000009b))
  inv_sbox[0x00000015] = Signal(intbv(0x0000002f))
  inv_sbox[0x00000016] = Signal(intbv(0x000000ff))
  inv_sbox[0x00000017] = Signal(intbv(0x00000087))
  inv_sbox[0x00000018] = Signal(intbv(0x00000034))
  inv_sbox[0x00000019] = Signal(intbv(0x0000008e))
  inv_sbox[0x0000001a] = Signal(intbv(0x00000043))
  inv_sbox[0x0000001b] = Signal(intbv(0x00000044))
  inv_sbox[0x0000001c] = Signal(intbv(0x000000c4))
  inv_sbox[0x0000001d] = Signal(intbv(0x000000de))
  inv_sbox[0x0000001e] = Signal(intbv(0x000000e9))
  inv_sbox[0x0000001f] = Signal(intbv(0x000000cb))
  inv_sbox[0x00000020] = Signal(intbv(0x00000054))
  inv_sbox[0x00000021] = Signal(intbv(0x0000007b))
  inv_sbox[0x00000022] = Signal(intbv(0x00000094))
  inv_sbox[0x00000023] = Signal(intbv(0x00000032))
  inv_sbox[0x00000024] = Signal(intbv(0x000000a6))
  inv_sbox[0x00000025] = Signal(intbv(0x000000c2))
  inv_sbox[0x00000026] = Signal(intbv(0x00000023))
  inv_sbox[0x00000027] = Signal(intbv(0x0000003d))
  inv_sbox[0x00000028] = Signal(intbv(0x000000ee))
  inv_sbox[0x00000029] = Signal(intbv(0x0000004c))
  inv_sbox[0x0000002a] = Signal(intbv(0x00000095))
  inv_sbox[0x0000002b] = Signal(intbv(0x0000000b))
  inv_sbox[0x0000002c] = Signal(intbv(0x00000042))
  inv_sbox[0x0000002d] = Signal(intbv(0x000000fa))
  inv_sbox[0x0000002e] = Signal(intbv(0x000000c3))
  inv_sbox[0x0000002f] = Signal(intbv(0x0000004e))
  inv_sbox[0x00000030] = Signal(intbv(0x00000008))
  inv_sbox[0x00000031] = Signal(intbv(0x0000002e))
  inv_sbox[0x00000032] = Signal(intbv(0x000000a1))
  inv_sbox[0x00000033] = Signal(intbv(0x00000066))
  inv_sbox[0x00000034] = Signal(intbv(0x00000028))
  inv_sbox[0x00000035] = Signal(intbv(0x000000d9))
  inv_sbox[0x00000036] = Signal(intbv(0x00000024))
  inv_sbox[0x00000037] = Signal(intbv(0x000000b2))
  inv_sbox[0x00000038] = Signal(intbv(0x00000076))
  inv_sbox[0x00000039] = Signal(intbv(0x0000005b))
  inv_sbox[0x0000003a] = Signal(intbv(0x000000a2))
  inv_sbox[0x0000003b] = Signal(intbv(0x00000049))
  inv_sbox[0x0000003c] = Signal(intbv(0x0000006d))
  inv_sbox[0x0000003d] = Signal(intbv(0x0000008b))
  inv_sbox[0x0000003e] = Signal(intbv(0x000000d1))
  inv_sbox[0x0000003f] = Signal(intbv(0x00000025))
  inv_sbox[0x00000040] = Signal(intbv(0x00000072))
  inv_sbox[0x00000041] = Signal(intbv(0x000000f8))
  inv_sbox[0x00000042] = Signal(intbv(0x000000f6))
  inv_sbox[0x00000043] = Signal(intbv(0x00000064))
  inv_sbox[0x00000044] = Signal(intbv(0x00000086))
  inv_sbox[0x00000045] = Signal(intbv(0x00000068))
  inv_sbox[0x00000046] = Signal(intbv(0x00000098))
  inv_sbox[0x00000047] = Signal(intbv(0x00000016))
  inv_sbox[0x00000048] = Signal(intbv(0x000000d4))
  inv_sbox[0x00000049] = Signal(intbv(0x000000a4))
  inv_sbox[0x0000004a] = Signal(intbv(0x0000005c))
  inv_sbox[0x0000004b] = Signal(intbv(0x000000cc))
  inv_sbox[0x0000004c] = Signal(intbv(0x0000005d))
  inv_sbox[0x0000004d] = Signal(intbv(0x00000065))
  inv_sbox[0x0000004e] = Signal(intbv(0x000000b6))
  inv_sbox[0x0000004f] = Signal(intbv(0x00000092))
  inv_sbox[0x00000050] = Signal(intbv(0x0000006c))
  inv_sbox[0x00000051] = Signal(intbv(0x00000070))
  inv_sbox[0x00000052] = Signal(intbv(0x00000048))
  inv_sbox[0x00000053] = Signal(intbv(0x00000050))
  inv_sbox[0x00000054] = Signal(intbv(0x000000fd))
  inv_sbox[0x00000055] = Signal(intbv(0x000000ed))
  inv_sbox[0x00000056] = Signal(intbv(0x000000b9))
  inv_sbox[0x00000057] = Signal(intbv(0x000000da))
  inv_sbox[0x00000058] = Signal(intbv(0x0000005e))
  inv_sbox[0x00000059] = Signal(intbv(0x00000015))
  inv_sbox[0x0000005a] = Signal(intbv(0x00000046))
  inv_sbox[0x0000005b] = Signal(intbv(0x00000057))
  inv_sbox[0x0000005c] = Signal(intbv(0x000000a7))
  inv_sbox[0x0000005d] = Signal(intbv(0x0000008d))
  inv_sbox[0x0000005e] = Signal(intbv(0x0000009d))
  inv_sbox[0x0000005f] = Signal(intbv(0x00000084))
  inv_sbox[0x00000060] = Signal(intbv(0x00000090))
  inv_sbox[0x00000061] = Signal(intbv(0x000000d8))
  inv_sbox[0x00000062] = Signal(intbv(0x000000ab))
  inv_sbox[0x00000063] = Signal(intbv(0x00000000))
  inv_sbox[0x00000064] = Signal(intbv(0x0000008c))
  inv_sbox[0x00000065] = Signal(intbv(0x000000bc))
  inv_sbox[0x00000066] = Signal(intbv(0x000000d3))
  inv_sbox[0x00000067] = Signal(intbv(0x0000000a))
  inv_sbox[0x00000068] = Signal(intbv(0x000000f7))
  inv_sbox[0x00000069] = Signal(intbv(0x000000e4))
  inv_sbox[0x0000006a] = Signal(intbv(0x00000058))
  inv_sbox[0x0000006b] = Signal(intbv(0x00000005))
  inv_sbox[0x0000006c] = Signal(intbv(0x000000b8))
  inv_sbox[0x0000006d] = Signal(intbv(0x000000b3))
  inv_sbox[0x0000006e] = Signal(intbv(0x00000045))
  inv_sbox[0x0000006f] = Signal(intbv(0x00000006))
  inv_sbox[0x00000070] = Signal(intbv(0x000000d0))
  inv_sbox[0x00000071] = Signal(intbv(0x0000002c))
  inv_sbox[0x00000072] = Signal(intbv(0x0000001e))
  inv_sbox[0x00000073] = Signal(intbv(0x0000008f))
  inv_sbox[0x00000074] = Signal(intbv(0x000000ca))
  inv_sbox[0x00000075] = Signal(intbv(0x0000003f))
  inv_sbox[0x00000076] = Signal(intbv(0x0000000f))
  inv_sbox[0x00000077] = Signal(intbv(0x00000002))
  inv_sbox[0x00000078] = Signal(intbv(0x000000c1))
  inv_sbox[0x00000079] = Signal(intbv(0x000000af))
  inv_sbox[0x0000007a] = Signal(intbv(0x000000bd))
  inv_sbox[0x0000007b] = Signal(intbv(0x00000003))
  inv_sbox[0x0000007c] = Signal(intbv(0x00000001))
  inv_sbox[0x0000007d] = Signal(intbv(0x00000013))
  inv_sbox[0x0000007e] = Signal(intbv(0x0000008a))
  inv_sbox[0x0000007f] = Signal(intbv(0x0000006b))
  inv_sbox[0x00000080] = Signal(intbv(0x0000003a))
  inv_sbox[0x00000081] = Signal(intbv(0x00000091))
  inv_sbox[0x00000082] = Signal(intbv(0x00000011))
  inv_sbox[0x00000083] = Signal(intbv(0x00000041))
  inv_sbox[0x00000084] = Signal(intbv(0x0000004f))
  inv_sbox[0x00000085] = Signal(intbv(0x00000067))
  inv_sbox[0x00000086] = Signal(intbv(0x000000dc))
  inv_sbox[0x00000087] = Signal(intbv(0x000000ea))
  inv_sbox[0x00000088] = Signal(intbv(0x00000097))
  inv_sbox[0x00000089] = Signal(intbv(0x000000f2))
  inv_sbox[0x0000008a] = Signal(intbv(0x000000cf))
  inv_sbox[0x0000008b] = Signal(intbv(0x000000ce))
  inv_sbox[0x0000008c] = Signal(intbv(0x000000f0))
  inv_sbox[0x0000008d] = Signal(intbv(0x000000b4))
  inv_sbox[0x0000008e] = Signal(intbv(0x000000e6))
  inv_sbox[0x0000008f] = Signal(intbv(0x00000073))
  inv_sbox[0x00000090] = Signal(intbv(0x00000096))
  inv_sbox[0x00000091] = Signal(intbv(0x000000ac))
  inv_sbox[0x00000092] = Signal(intbv(0x00000074))
  inv_sbox[0x00000093] = Signal(intbv(0x00000022))
  inv_sbox[0x00000094] = Signal(intbv(0x000000e7))
  inv_sbox[0x00000095] = Signal(intbv(0x000000ad))
  inv_sbox[0x00000096] = Signal(intbv(0x00000035))
  inv_sbox[0x00000097] = Signal(intbv(0x00000085))
  inv_sbox[0x00000098] = Signal(intbv(0x000000e2))
  inv_sbox[0x00000099] = Signal(intbv(0x000000f9))
  inv_sbox[0x0000009a] = Signal(intbv(0x00000037))
  inv_sbox[0x0000009b] = Signal(intbv(0x000000e8))
  inv_sbox[0x0000009c] = Signal(intbv(0x0000001c))
  inv_sbox[0x0000009d] = Signal(intbv(0x00000075))
  inv_sbox[0x0000009e] = Signal(intbv(0x000000df))
  inv_sbox[0x0000009f] = Signal(intbv(0x0000006e))
  inv_sbox[0x000000a0] = Signal(intbv(0x00000047))
  inv_sbox[0x000000a1] = Signal(intbv(0x000000f1))
  inv_sbox[0x000000a2] = Signal(intbv(0x0000001a))
  inv_sbox[0x000000a3] = Signal(intbv(0x00000071))
  inv_sbox[0x000000a4] = Signal(intbv(0x0000001d))
  inv_sbox[0x000000a5] = Signal(intbv(0x00000029))
  inv_sbox[0x000000a6] = Signal(intbv(0x000000c5))
  inv_sbox[0x000000a7] = Signal(intbv(0x00000089))
  inv_sbox[0x000000a8] = Signal(intbv(0x0000006f))
  inv_sbox[0x000000a9] = Signal(intbv(0x000000b7))
  inv_sbox[0x000000aa] = Signal(intbv(0x00000062))
  inv_sbox[0x000000ab] = Signal(intbv(0x0000000e))
  inv_sbox[0x000000ac] = Signal(intbv(0x000000aa))
  inv_sbox[0x000000ad] = Signal(intbv(0x00000018))
  inv_sbox[0x000000ae] = Signal(intbv(0x000000be))
  inv_sbox[0x000000af] = Signal(intbv(0x0000001b))
  inv_sbox[0x000000b0] = Signal(intbv(0x000000fc))
  inv_sbox[0x000000b1] = Signal(intbv(0x00000056))
  inv_sbox[0x000000b2] = Signal(intbv(0x0000003e))
  inv_sbox[0x000000b3] = Signal(intbv(0x0000004b))
  inv_sbox[0x000000b4] = Signal(intbv(0x000000c6))
  inv_sbox[0x000000b5] = Signal(intbv(0x000000d2))
  inv_sbox[0x000000b6] = Signal(intbv(0x00000079))
  inv_sbox[0x000000b7] = Signal(intbv(0x00000020))
  inv_sbox[0x000000b8] = Signal(intbv(0x0000009a))
  inv_sbox[0x000000b9] = Signal(intbv(0x000000db))
  inv_sbox[0x000000ba] = Signal(intbv(0x000000c0))
  inv_sbox[0x000000bb] = Signal(intbv(0x000000fe))
  inv_sbox[0x000000bc] = Signal(intbv(0x00000078))
  inv_sbox[0x000000bd] = Signal(intbv(0x000000cd))
  inv_sbox[0x000000be] = Signal(intbv(0x0000005a))
  inv_sbox[0x000000bf] = Signal(intbv(0x000000f4))
  inv_sbox[0x000000c0] = Signal(intbv(0x0000001f))
  inv_sbox[0x000000c1] = Signal(intbv(0x000000dd))
  inv_sbox[0x000000c2] = Signal(intbv(0x000000a8))
  inv_sbox[0x000000c3] = Signal(intbv(0x00000033))
  inv_sbox[0x000000c4] = Signal(intbv(0x00000088))
  inv_sbox[0x000000c5] = Signal(intbv(0x00000007))
  inv_sbox[0x000000c6] = Signal(intbv(0x000000c7))
  inv_sbox[0x000000c7] = Signal(intbv(0x00000031))
  inv_sbox[0x000000c8] = Signal(intbv(0x000000b1))
  inv_sbox[0x000000c9] = Signal(intbv(0x00000012))
  inv_sbox[0x000000ca] = Signal(intbv(0x00000010))
  inv_sbox[0x000000cb] = Signal(intbv(0x00000059))
  inv_sbox[0x000000cc] = Signal(intbv(0x00000027))
  inv_sbox[0x000000cd] = Signal(intbv(0x00000080))
  inv_sbox[0x000000ce] = Signal(intbv(0x000000ec))
  inv_sbox[0x000000cf] = Signal(intbv(0x0000005f))
  inv_sbox[0x000000d0] = Signal(intbv(0x00000060))
  inv_sbox[0x000000d1] = Signal(intbv(0x00000051))
  inv_sbox[0x000000d2] = Signal(intbv(0x0000007f))
  inv_sbox[0x000000d3] = Signal(intbv(0x000000a9))
  inv_sbox[0x000000d4] = Signal(intbv(0x00000019))
  inv_sbox[0x000000d5] = Signal(intbv(0x000000b5))
  inv_sbox[0x000000d6] = Signal(intbv(0x0000004a))
  inv_sbox[0x000000d7] = Signal(intbv(0x0000000d))
  inv_sbox[0x000000d8] = Signal(intbv(0x0000002d))
  inv_sbox[0x000000d9] = Signal(intbv(0x000000e5))
  inv_sbox[0x000000da] = Signal(intbv(0x0000007a))
  inv_sbox[0x000000db] = Signal(intbv(0x0000009f))
  inv_sbox[0x000000dc] = Signal(intbv(0x00000093))
  inv_sbox[0x000000dd] = Signal(intbv(0x000000c9))
  inv_sbox[0x000000de] = Signal(intbv(0x0000009c))
  inv_sbox[0x000000df] = Signal(intbv(0x000000ef))
  inv_sbox[0x000000e0] = Signal(intbv(0x000000a0))
  inv_sbox[0x000000e1] = Signal(intbv(0x000000e0))
  inv_sbox[0x000000e2] = Signal(intbv(0x0000003b))
  inv_sbox[0x000000e3] = Signal(intbv(0x0000004d))
  inv_sbox[0x000000e4] = Signal(intbv(0x000000ae))
  inv_sbox[0x000000e5] = Signal(intbv(0x0000002a))
  inv_sbox[0x000000e6] = Signal(intbv(0x000000f5))
  inv_sbox[0x000000e7] = Signal(intbv(0x000000b0))
  inv_sbox[0x000000e8] = Signal(intbv(0x000000c8))
  inv_sbox[0x000000e9] = Signal(intbv(0x000000eb))
  inv_sbox[0x000000ea] = Signal(intbv(0x000000bb))
  inv_sbox[0x000000eb] = Signal(intbv(0x0000003c))
  inv_sbox[0x000000ec] = Signal(intbv(0x00000083))
  inv_sbox[0x000000ed] = Signal(intbv(0x00000053))
  inv_sbox[0x000000ee] = Signal(intbv(0x00000099))
  inv_sbox[0x000000ef] = Signal(intbv(0x00000061))
  inv_sbox[0x000000f0] = Signal(intbv(0x00000017))
  inv_sbox[0x000000f1] = Signal(intbv(0x0000002b))
  inv_sbox[0x000000f2] = Signal(intbv(0x00000004))
  inv_sbox[0x000000f3] = Signal(intbv(0x0000007e))
  inv_sbox[0x000000f4] = Signal(intbv(0x000000ba))
  inv_sbox[0x000000f5] = Signal(intbv(0x00000077))
  inv_sbox[0x000000f6] = Signal(intbv(0x000000d6))
  inv_sbox[0x000000f7] = Signal(intbv(0x00000026))
  inv_sbox[0x000000f8] = Signal(intbv(0x000000e1))
  inv_sbox[0x000000f9] = Signal(intbv(0x00000069))
  inv_sbox[0x000000fa] = Signal(intbv(0x00000014))
  inv_sbox[0x000000fb] = Signal(intbv(0x00000063))
  inv_sbox[0x000000fc] = Signal(intbv(0x00000055))
  inv_sbox[0x000000fd] = Signal(intbv(0x00000021))
  inv_sbox[0x000000fe] = Signal(intbv(0x0000000c))
  inv_sbox[0x000000ff] = Signal(intbv(0x0000007d))

  return inv_sbox


# //======================================================================
# // EOF aes_inv_sbox.v
# //======================================================================