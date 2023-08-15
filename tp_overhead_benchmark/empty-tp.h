#undef TRACEPOINT_PROVIDER
#define TRACEPOINT_PROVIDER empty_tp

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./empty-tp.h"

#if !defined(_EMPTY_TP_H) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _EMPTY_TP_H

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    empty_tp,
    my_first_tracepoint,
    TP_ARGS(
        int, my_integer_arg,
        char*, my_string_arg
    ),
    TP_FIELDS(
        ctf_string(my_string_field, my_string_arg)
        ctf_integer(int, my_integer_field, my_integer_arg)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_4b,
    TP_ARGS(
        int, payload
    ),
    TP_FIELDS(
        ctf_integer(int, payload_field, payload)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_16b,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 16)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_64b,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 64)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_256b,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 256)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_512b,
    TP_ARGS(
        char*, p1,
        char*, p2
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_1k,
    TP_ARGS(
        char*, p1,
        char*, p2,
        char*, p3,
        char*, p4
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
        ctf_array_text(char, p3_field, p3, 256)
        ctf_array_text(char, p4_field, p4, 256)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_2k,
    TP_ARGS(
        char*, p1,
        char*, p2,
        char*, p3,
        char*, p4,
        char*, p5,
        char*, p6,
        char*, p7,
        char*, p8
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
        ctf_array_text(char, p3_field, p3, 256)
        ctf_array_text(char, p4_field, p4, 256)
        ctf_array_text(char, p5_field, p5, 256)
        ctf_array_text(char, p6_field, p6, 256)
        ctf_array_text(char, p7_field, p7, 256)
        ctf_array_text(char, p8_field, p8, 256)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_4b_2,
    TP_ARGS(
        int, payload
    ),
    TP_FIELDS(
        ctf_integer(int, payload_field, payload)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_16b_2,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 16)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_64b_2,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 64)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_256b_2,
    TP_ARGS(
        char*, payload
    ),
    TP_FIELDS(
        ctf_array_text(char, payload_field, payload, 256)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_512b_2,
    TP_ARGS(
        char*, p1,
        char*, p2
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
    )
)

TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_1k_2,
    TP_ARGS(
        char*, p1,
        char*, p2,
        char*, p3,
        char*, p4
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
        ctf_array_text(char, p3_field, p3, 256)
        ctf_array_text(char, p4_field, p4, 256)
    )
)


TRACEPOINT_EVENT(
    empty_tp,
    empty_tp_2k_2,
    TP_ARGS(
        char*, p1,
        char*, p2,
        char*, p3,
        char*, p4,
        char*, p5,
        char*, p6,
        char*, p7,
        char*, p8
    ),
    TP_FIELDS(
        ctf_array_text(char, p1_field, p1, 256)
        ctf_array_text(char, p2_field, p2, 256)
        ctf_array_text(char, p3_field, p3, 256)
        ctf_array_text(char, p4_field, p4, 256)
        ctf_array_text(char, p5_field, p5, 256)
        ctf_array_text(char, p6_field, p6, 256)
        ctf_array_text(char, p7_field, p7, 256)
        ctf_array_text(char, p8_field, p8, 256)
    )
)



#endif /* _EMPTY_TP_H */

#include <lttng/tracepoint-event.h>