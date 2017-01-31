#include <stdint.h>
#include <string.h>

uint32_t crc32_table[255];


uint32_t crc_chained(uint32_t basecrc, uint8_t *message, uint32_t datasize)
{
    /* Through with table setup, now calculate the CRC. */
    uint8_t i, byte;
    uint32_t crc, mask;

    for (byte = 0; byte < 255; byte++)
    {
        crc = byte;
        for (i = 8; i > 0; i--)
        {  // Do eight times.
            mask = -(crc & 1);
            crc = (crc >> 1) ^ (0xEDB88320 & mask);
        }
        crc32_table[byte] = crc;
    }

    i = 0;
    crc = basecrc;
    for (i=0;i<datasize; i++)
    {
        byte=message[i];
        crc = (crc >> 8) ^ crc32_table[(crc ^ byte) & 0xFF];
    }
    return (~crc);
}

