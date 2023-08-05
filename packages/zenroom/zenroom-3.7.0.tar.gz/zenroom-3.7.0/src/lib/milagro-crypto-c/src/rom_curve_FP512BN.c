/*
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
*/

#include "arch.h"
#include "ecp_FP512BN.h"

/* Curve FP512BN - Pairing friendly BN curve */

/* ISO curve */

#if CHUNK==16

#error Not supported

#endif

#if CHUNK==32

const int CURVE_Cof_I_FP512BN= 1;
const int CURVE_A_FP512BN= 0;
const int CURVE_B_I_FP512BN= 3;
const BIG_512_29 CURVE_B_FP512BN= {0x3,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};
const BIG_512_29 CURVE_Order_FP512BN= {0x119A09ED,0x153252FA,0x1E68AD01,0x627C09,0x79A34A1,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF};
const BIG_512_29 CURVE_Gx_FP512BN= {0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};
const BIG_512_29 CURVE_Gy_FP512BN= {0x2,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};

const BIG_512_29 CURVE_Bnx_FP512BN= {0x1E1BD80F,0x59835DA,0xC3DFC04,0x5EB8061,0x688,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};
const BIG_512_29 CURVE_Cof_FP512BN= {0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};

const BIG_512_29 CURVE_Cru_FP512BN= {0x1C79298A,0x1838B104,0x2C5F052,0x1DCCF337,0x6092AEC,0x4B35F29,0x1EB361E,0x11384EA,0x3074B20,0x17BB08FD,0x3A8B3E3,0xD70D66F,0x3D2A614,0x1CF63EE4,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF};

const BIG_512_29 CURVE_Pxa_FP512BN= {0xDB646B5,0x183D4B70,0x1CBFFA3,0x11F0E632,0x1C78F221,0x1F10DE5D,0x171B715E,0xF0C6A29,0x10B02453,0xBE63C66,0xE6D5F69,0x166B1E1B,0x4BBBD29,0x179E750F,0x6E9D04,0xC912B10,0x1339E138,0x1D8B2};
const BIG_512_29 CURVE_Pxb_FP512BN= {0x1A8AE0E9,0xDAE5F7E,0x22446CF,0x1948239B,0x15ADCE40,0xB709C1E,0x18357943,0xE50AA4D,0x19781E22,0x12B35CA6,0x11DAA2C0,0x18D8DDE4,0x5EA656D,0x15F45A41,0xD311A02,0xCFCD913,0x13CBF850,0x240E0};
const BIG_512_29 CURVE_Pya_FP512BN= {0xDDE67A1,0x12401895,0x17BEE178,0x142F5AC2,0xB7BC5CD,0x92A1404,0x1A3B748C,0x17BD82A7,0x14B6CD18,0xAC34CE,0x1740FB97,0x1ECC15F9,0x17085B1D,0x1D1BA793,0x1BD6AC32,0x18F70525,0xC84C827,0x3780F};
const BIG_512_29 CURVE_Pyb_FP512BN= {0x84F8E8B,0xC5B8C36,0xFDD85A1,0xB84449,0x19C08DFF,0x56BF713,0x1C5290C4,0x187C5CA0,0x1DA2897F,0x24B0CA0,0x326D8F4,0x2310CF6,0x1021438C,0xFBAEC8F,0xD9030C5,0x1CF06358,0x1CEC8B04,0x28D1D};
const BIG_512_29 CURVE_W_FP512BN[2]= {{0x9834583,0x887C4BA,0x5A85CFC,0xBF7223A,0xF63FE96,0x1FFFFFFE,0x1FFFFFFF,0x1FFFFFFF,0xFFFFFF,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},{0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0}};
const BIG_512_29 CURVE_SB_FP512BN[2][2]= {{{0xD4B9564,0x1D575904,0xD2C64F3,0x202177,0xF63F186,0x1FFFFFFE,0x1FFFFFFF,0x1FFFFFFF,0xFFFFFF,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},{0x156259CE,0xA01E744,0x5ECB4F9,0x148B7B47,0x79A2790,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF}},{{0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},{0x9834583,0x887C4BA,0x5A85CFC,0xBF7223A,0xF63FE96,0x1FFFFFFE,0x1FFFFFFF,0x1FFFFFFF,0xFFFFFF,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0}}};
const BIG_512_29 CURVE_WB_FP512BN[4]= {{0x155A29F0,0x16D59B55,0xF4C305,0x18858C0B,0x5215FBF,0xAAAAAAA,0x15555555,0xAAAAAAA,0x555555,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},{0x2355D4B,0x1758095D,0x1FE13C5F,0x41F83FA,0xBB5E5CF,0x97D4EF1,0xB503D62,0x172C0C9B,0x16315274,0x15E1A9A8,0x859835D,0x2C3DFC0,0x105EB806,0x68,0x0,0x0,0x0,0x0},{0x289AAD,0x1E781F9C,0x60F9C31,0x1505822E,0x15DAF62B,0x4BEA778,0x15A81EB1,0xB96064D,0xB18A93A,0x1AF0D4D4,0x42CC1AE,0x161EFE0,0x82F5C03,0x34,0x0,0x0,0x0,0x0},{0x192279D1,0xBA52F9F,0x878CAFD,0xCAE8B48,0x52152AF,0xAAAAAAA,0x15555555,0xAAAAAAA,0x555555,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0}};
const BIG_512_29 CURVE_BB_FP512BN[4][4]= {{{0x1E1BD810,0x59835DA,0xC3DFC04,0x5EB8061,0x688,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x1E1BD80F,0x59835DA,0xC3DFC04,0x5EB8061,0x688,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x1E1BD80F,0x59835DA,0xC3DFC04,0x5EB8061,0x688,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x156259CF,0xA01E744,0x5ECB4F9,0x148B7B47,0x79A2790,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF}
    },
    {   {0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x137E31DE,0xF9A1D1F,0x122AB0FD,0x1A76FBA8,0x79A2E18,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF},
        {0x137E31DD,0xF9A1D1F,0x122AB0FD,0x1A76FBA8,0x79A2E18,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF},
        {0x137E31DE,0xF9A1D1F,0x122AB0FD,0x1A76FBA8,0x79A2E18,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF}
    },
    {   {0x1C37B01E,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x1C37B01F,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0}
    },
    {   {0x137E31DF,0xF9A1D1F,0x122AB0FD,0x1A76FBA8,0x79A2E18,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF},
        {0x192AA9AF,0x1ED17B8E,0xD70BCF0,0x8B47A84,0x79A1A80,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF},
        {0x1C37B01D,0xB306BB5,0x187BF808,0xBD700C2,0xD10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0},
        {0x137E31DF,0xF9A1D1F,0x122AB0FD,0x1A76FBA8,0x79A2E18,0x12EF5593,0x2E39231,0x3D597D3,0x45146CF,0x88D877A,0x102EF8F0,0x1196A60F,0x1C60BA1D,0x1CF63F80,0x1FFFFFFF,0x1FFFFFFF,0x1FFFFFFF,0x7FFFF}
    }
};


#endif

#if CHUNK==64

const int CURVE_Cof_I_FP512BN= 1;
const int CURVE_A_FP512BN= 0;
const int CURVE_B_I_FP512BN= 3;
const BIG_512_60 CURVE_B_FP512BN= {0x3L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L};
const BIG_512_60 CURVE_Order_FP512BN= {0x6A64A5F519A09EDL,0x10313E04F9A2B40L,0xC65DEAB2679A34AL,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL};
const BIG_512_60 CURVE_Gx_FP512BN= {0x1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L};
const BIG_512_60 CURVE_Gy_FP512BN= {0x2L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L};

const BIG_512_60 CURVE_Bnx_FP512BN= {0xB306BB5E1BD80FL,0x82F5C030B0F7F01L,0x68L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L};
const BIG_512_60 CURVE_Cof_FP512BN= {0x1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L};

const BIG_512_60 CURVE_Cru_FP512BN= {0xB0716209C79298AL,0xCEE6799B8B17C14L,0x78966BE526092AEL,0x20089C27507ACD8L,0xF8EF7611FA3074BL,0x6146B86B378EA2CL,0xFFFF9EC7DC83D2AL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL};

const BIG_512_60 CURVE_Pxa_FP512BN= {0xF07A96E0DB646B5L,0x18F87319072FFE8L,0x7BE21BCBBC78F22L,0x537863514DC6DC5L,0xDA57CC78CD0B024L,0xD29B358F0DB9B57L,0x7412F3CEA1E4BBBL,0xE138648958801BAL,0x3B165339L};
const BIG_512_60 CURVE_Pxb_FP512BN= {0xDB5CBEFDA8AE0E9L,0xCA411CD88911B3L,0xD6E1383D5ADCE4L,0x227285526E0D5E5L,0xB02566B94D9781EL,0x56DC6C6EF2476A8L,0x680ABE8B4825EA6L,0xF85067E6C89B4C4L,0x481C13CBL};
const BIG_512_60 CURVE_Pya_FP512BN= {0x2480312ADDE67A1L,0xDA17AD615EFB85EL,0x312542808B7BC5CL,0x18BDEC153E8EDD2L,0xE5C158699D4B6CDL,0xB1DF660AFCDD03EL,0xB0CBA374F277085L,0xC827C7B8292EF5AL,0x6F01EC84L};
const BIG_512_60 CURVE_Pyb_FP512BN= {0x58B7186C84F8E8BL,0xF05C2224BF76168L,0x10AD7EE279C08DFL,0x7FC3E2E50714A43L,0x3D04961941DA289L,0x38C118867B0C9B6L,0xC315F75D91F0214L,0x8B04E7831AC3640L,0x51A3BCECL};
const BIG_512_60 CURVE_W_FP512BN[2]= {{0x110F89749834583L,0x65FB911D16A173FL,0xFFFFFFFFCF63FE9L,0xFFFFFFFFFFFFFFFL,0xFFFFL,0x0L,0x0L,0x0L,0x0L},{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L}};
const BIG_512_60 CURVE_SB_FP512BN[2][2]= {{{0xFAAEB208D4B9564L,0x601010BBB4B193CL,0xFFFFFFFFCF63F18L,0xFFFFFFFFFFFFFFFL,0xFFFFL,0x0L,0x0L,0x0L,0x0L},{0x5403CE8956259CEL,0xA45BDA397B2D3EL,0xC65DEAB2679A279L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL}},{{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x110F89749834583L,0x65FB911D16A173FL,0xFFFFFFFFCF63FE9L,0xFFFFFFFFFFFFFFFL,0xFFFFL,0x0L,0x0L,0x0L,0x0L}}};
const BIG_512_60 CURVE_WB_FP512BN[4]= {{0x6DAB36AB55A29F0L,0xFC42C60583D30C1L,0x5555555545215FBL,0x555555555555555L,0x5555L,0x0L,0x0L,0x0L,0x0L},{0xEEB012BA2355D4BL,0xF20FC1FD7F84F17L,0x892FA9DE2BB5E5CL,0x74B96064DAD40F5L,0xD76BC3535163152L,0x806161EFE021660L,0xD105EBL,0x0L,0x0L},{0x7CF03F380289AADL,0xBA82C117183E70CL,0xC497D4EF15DAF62L,0x3A5CB0326D6A07AL,0x6BB5E1A9A8B18A9L,0xC030B0F7F010B30L,0x6882F5L,0x0L,0x0L},{0x574A5F3F92279D1L,0xF65745A421E32BFL,0x55555555452152AL,0x555555555555555L,0x5555L,0x0L,0x0L,0x0L,0x0L}};
const BIG_512_60 CURVE_BB_FP512BN[4][4]= {{{0xB306BB5E1BD810L,0x82F5C030B0F7F01L,0x68L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0xB306BB5E1BD80FL,0x82F5C030B0F7F01L,0x68L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0xB306BB5E1BD80FL,0x82F5C030B0F7F01L,0x68L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x5403CE8956259CFL,0xA45BDA397B2D3EL,0xC65DEAB2679A279L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL}},{{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x5F343A3F37E31DEL,0x8D3B7DD448AAC3FL,0xC65DEAB2679A2E1L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL},{0x5F343A3F37E31DDL,0x8D3B7DD448AAC3FL,0xC65DEAB2679A2E1L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL},{0x5F343A3F37E31DEL,0x8D3B7DD448AAC3FL,0xC65DEAB2679A2E1L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL}},{{0x1660D76BC37B01EL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x1660D76BC37B01FL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L}},{{0x5F343A3F37E31DFL,0x8D3B7DD448AAC3FL,0xC65DEAB2679A2E1L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL},{0x3DA2F71D92AA9AFL,0x45A3D4235C2F3CL,0xC65DEAB2679A1A8L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL},{0x1660D76BC37B01DL,0x5EB806161EFE02L,0xD1L,0x0L,0x0L,0x0L,0x0L,0x0L,0x0L},{0x5F343A3F37E31DFL,0x8D3B7DD448AAC3FL,0xC65DEAB2679A2E1L,0xCF1EACBE98B8E48L,0x3C111B0EF445146L,0xA1D8CB5307C0BBEL,0xFFFF9EC7F01C60BL,0xFFFFFFFFFFFFFFFL,0xFFFFFFFFL}}};


#endif

