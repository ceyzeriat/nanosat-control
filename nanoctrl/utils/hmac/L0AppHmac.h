/*
 * hmac.h
 *
 *  Created on: 21 mars 2017
 *      Author: acrouzier
 */

#ifndef _L0APP_HMAC_H_
#define _L0APP_HMAC_H_

#include <stdint.h>

//#include <obc/demo1/l0app/L0CryptoLib/L0AppSha256.h>
#define SHA256_DIGEST_SIZE 32   // SHA256 outputs a 32 byte digest
#define SHA256_BLOCK_SIZE 32 // SHA256 uses a 32 bytes block size, the key size must be the same
#define MAX_MESSAGE_SIZE 256
// todo: temp key: in final version chose proper key
#define HMAC_KEY {0xd6 ,0x53 ,0x37 ,0x10 ,0x1b ,0x3a ,0xde ,0x40 ,0xe0 ,0x59 ,0x1e ,0xa6 ,0x52 ,0xe7 ,0x16 ,0x57 ,0xb6 ,0x04 ,0xe5 ,0x3f ,0x64 ,0x1a ,0xa9 ,0x41 ,0x23 ,0x1a ,0xe2 ,0x82 ,0x1b ,0xae ,0x91 ,0xa5}
// random hashes (used to generate temp key)
// 857103618c4f2e9278040857475550d6533fa31bf754409f31b3adb2911e1e62
// c4a6deed9f9e40e0524e389a39f82711ba65946d144512ec6f221ea63ecf52e7
// fd70f1657b6cd35a80db9ab37c8010de49d3b9db1c9dfb7b07137f904e7327d6
// 53f62fe433a53ae5faaa55bd4120a4812d741793d7b30b526389c610ca721175
// 48bae932db9bd1a5b297745acf12aa9412f92b99b28cd31ae5282821fc434f55

// key length: 32 bytes
// message size is free
// digest size: 32 bytes
void hmacSha256(const unsigned char* key, const unsigned char* message, unsigned int messageLength, unsigned char* digest);

void printBytesGrid16(uint8_t* buffer, uint16_t length);

#endif /* _L0APP_HMAC_H_ */
