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
#include "fp_BLS461.h"

/* Curve BLS461 - Pairing friendly BLS curve */

#if CHUNK==16

#error Not supported

#endif

#if CHUNK==32
// Base Bits= 28
const BIG_464_28 Modulus_BLS461= {0xAAAAAAB,0xAC0000A,0x54AAAAA,0x5555,0x400020,0x91557F0,0xF26AA,0xFA5C1CC,0xB42A8DF,0x7B14848,0x8BACCA4,0x6F1E32D,0x4935FBD,0x55D6941,0xD5A555A,0x5545554,0x1555};
const BIG_464_28 R2modp_BLS461= {0xC9B6A33,0x2ECD087,0x3CCB2B1,0xCD461FE,0x8CB5AB2,0xC5B9635,0x5312E92,0xB659F64,0x3B596FA,0x8679006,0xA92E2B3,0x3CE05E3,0x363550F,0x7C07A8E,0x382C083,0x6347FEA,0xBD};
const chunk MConst_BLS461= 0xFFFFFFD;
const BIG_464_28 Fra_BLS461= {0xB812A3A,0x7117BF9,0x99C400F,0xC6308A5,0x5BF8A1,0x510E075,0x45FA5A6,0xCE4858D,0x770B31A,0xBC2CB04,0xE2FC61E,0xD073588,0x4366190,0x4DFEFA8,0x69E55E2,0x504B7F,0x12E4};
const BIG_464_28 Frb_BLS461= {0xF298071,0x3AE8410,0xBAE6A9B,0x39D4CAF,0xFE4077E,0x404777A,0xBAF8104,0x2C13C3E,0x3D1F5C5,0xBEE7D44,0xA8B0685,0x9EAADA4,0x5CFE2C,0x7D7999,0x6BBFF78,0x50409D5,0x271};

#endif

#if CHUNK==64
// Base Bits=60
const BIG_464_60 Modulus_BLS461= {0xAAC0000AAAAAAABL,0x20000555554AAAAL,0x6AA91557F004000L,0xA8DFFA5C1CC00F2L,0xACCA47B14848B42L,0x935FBD6F1E32D8BL,0xD5A555A55D69414L,0x15555545554L};
const BIG_464_60 R2modp_BLS461= {0x96D08774614DDA8L,0xCD45F539225D5BDL,0xD712EB760C95AB1L,0xB3B687155F30B55L,0xC4E62A05C3F5B81L,0xBA1151676CA3CD0L,0x7EDD8A958F442BEL,0x12B89DD3F91L};
const chunk MConst_BLS461= 0xC0005FFFFFFFDL;
const BIG_464_60 Fra_BLS461= {0xF7117BF9B812A3AL,0xA1C6308A599C400L,0x5A6510E07505BF8L,0xB31ACE4858D45FAL,0xFC61EBC2CB04770L,0x366190D073588E2L,0x69E55E24DFEFA84L,0x12E40504B7FL};
const BIG_464_60 Frb_BLS461= {0xB3AE8410F298071L,0x7E39D4CAFBAE6A9L,0x104404777AFE407L,0xF5C52C13C3EBAF8L,0xB0685BEE7D443D1L,0x5CFE2C9EAADA4A8L,0x6BBFF7807D79990L,0x27150409D5L};


#endif
