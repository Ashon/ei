def serialize_data_as_list(headers, results):
    return [
        [k[1](v.get(k[0], '')) for k in headers] for v in results
    ]


def serialize_data_as_dict(headers, result):
    return {
        header[0]: header[1](result.get(header[0], ''))
        for header in headers
    }
