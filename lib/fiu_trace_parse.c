#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

/*
 * If the fp string size is 32 set
 * it to 1(webmail, cheeta), or 0 for 256(homes)
 */
#if 0
#define FP_STRING 33
#define FP  16
#define LOGO_FP 19
#define LOGO_FP_PLUS_1 20
#else
#define FP_STRING 257
#define FP  128
#define LOGO_FP 131
#define LOGO_FP_PLUS_1 132
#endif

#define PAGE_SIZE   4096
#define READ            1
#define WRITE           0
#define DATA_SIZE       400

#define VERBOSE 1

#if VERBOSE
#define DPRINTF( s, arg... ) printf( s , ##arg)
#else
#define DPRINTF( s, arg... )
#endif

/* Trace information */
struct trace_info {
   unsigned long long sector;	// request source address
   unsigned long long size;	// request size (unit is sector)
   int rw;			// 1 is read 0 is write
   unsigned char fp[FP];	// fingerprint buffer
};

/* Fingerprint copy function */
void fpcpy(char *md5, unsigned char *fingerprint)
{
    int i;
    char tmp[3];
    for (i = 0; i < FP; i++) {
        memcpy(tmp, (md5 + i * 2), 2);
        tmp[2] = '\0';
        sscanf(tmp, "%X", (unsigned int *)(fingerprint + i));
    }
}

int main(int argc, char *argv[])
{
    char buffer[DATA_SIZE];
    char fp_buf[FP_STRING];
    FILE *ifd;
    char *buf;
    char *result;
    int i, j;
    struct trace_info info;

    printf("Open file %s\n", argv[1]);
    ifd = fopen(argv[1], "r");

    while(1) {
        if (fgets(buffer, DATA_SIZE, ifd) == NULL){
            printf("The parse is done.\n");
            break;
        }

//      DPRINTF("Traces: %s\n", buffer);
        buf = buffer;
        i = 0;
        while((result = strsep(&buf, " ")) != NULL){
            switch (i) {
                case 3:
                    sscanf(result, "%llu", &info.sector);
                    break;
                case 4:
                    sscanf(result, "%llu", &info.size);
                    break;
                case 5:
                    info.rw = (!strcmp(result, "R"))? 1 : 0 ;
                    break;
                case 8:
                    result[FP_STRING - 1] = '\0';
                    strcpy(fp_buf, result);
                    fp_buf[FP_STRING - 1] = '\0';
                    fpcpy(fp_buf, info.fp);
                    break;
            }
            i++;
        }
        //DPRINTF("sector=%llu rw=%d size=%llu fp=", info.sector, info.rw, info.size);
			   DPRINTF("%lld\n", info.sector);
        //for (j = 0; j < FP; j++) {
        //    DPRINTF("%02x", info.fp[j]);
        //}
        //DPRINTF("\n");
    }
    return 1;
}
