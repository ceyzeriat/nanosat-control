/*
 * L0AppHmac.c
 *
 *  Created on: 21 mars 2017
 *      Author: acrouzier
 */

#include <stdio.h>
#include "L0AppHmac.h"
#include "L0AppSha256.h"
#include <stdint.h>

// key length must be = SHA256_BLOCK_SIZE
// digest length = SHA256_BLOCK_SIZE = 32
// message length is free
void hmacSha256(const unsigned char* key, const unsigned char* message, const unsigned int messageLength, unsigned char* digest){

	int i =0;
	unsigned char hashInput1[SHA256_BLOCK_SIZE+MAX_MESSAGE_SIZE];
	unsigned char hashInput2[2*SHA256_BLOCK_SIZE];

	//printf("message (in func):\r\n");
	//printBytesGrid16(message, messageLength);
	
	/*******************************************/
	/* SHA iteration 1 */
	for(i=0; i < SHA256_BLOCK_SIZE; i++){
		hashInput1[i] = key[i];
	}
	for(i=SHA256_BLOCK_SIZE; i < SHA256_BLOCK_SIZE+messageLength; i++){
		hashInput1[i] = message[i-SHA256_BLOCK_SIZE];
		//printf("%02X ", message[i-SHA256_BLOCK_SIZE]);
	}
	//printf("\r\n");
	
	
	//printf("hashInput1:\r\n");
	//printBytesGrid16(hashInput1, SHA256_BLOCK_SIZE+messageLength);
	mbedtls_sha256( hashInput1, SHA256_BLOCK_SIZE+messageLength, digest, 0); // 1st hash call
	//printf("sha256_iter1:\r\n");
	//printBytesGrid16(digest, SHA256_BLOCK_SIZE);
		
	/*******************************************/

	/*******************************************/
	/* SHA iteration 2 */
	for(i=0; i < SHA256_BLOCK_SIZE; i++){
		hashInput2[i] = key[i];
	}
	for(i=SHA256_BLOCK_SIZE; i < 2*SHA256_BLOCK_SIZE; i++){
		hashInput2[i] = digest[i-SHA256_BLOCK_SIZE];
	}
	
	//printf("hashInput2:\r\n");
	//printBytesGrid16(hashInput2, 2*SHA256_DIGEST_SIZE);
	mbedtls_sha256( hashInput2, 2*SHA256_BLOCK_SIZE, digest, 0); // 2nd hash call
	//printf("sha256_iter2:\r\n");
	//printBytesGrid16(digest, SHA256_DIGEST_SIZE);
	/*******************************************/
}

void printBytesGrid16(uint8_t* buffer, uint16_t length){
	printf("Index:  0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F\r\n");
	int cMax = length;
	int r;
	int i;
	if(cMax < 16) cMax = 16;
	for(r = 0; r <= (length-1)/16; r++){ // loop on rows
		printf("%02X:     ",r);
		for(i = 16*r; i < 16*(r+1); i++){ // loop on indexes
			if(i < length) printf("%02X ",buffer[i]);
		}
		printf("\r\n");
	}
}


