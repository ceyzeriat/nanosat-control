#ifndef _L0APPCRC32_H_
#define _L0APPCRC32_H_

#include <stdint.h>
#include <string.h>


uint32_t crc_chained(uint32_t basecrc, uint8_t *message, uint32_t datasize);


#endif
