Compile parcer:
    gcc fiu_trace_parse.c -o trace_parse


Run MARKING algorithm using trace data:
    ./trace_parse [datafile] | python3 MARKING.py
