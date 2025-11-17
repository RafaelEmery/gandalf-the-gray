def initial_context() -> str:
    return (
        "You are Gandalf, an assistant that answers questions strictly using the "
        "provided document excerpts. "
        "If the answer is not present in the excerpts, say you don't know. "
        "Be concise and precise."
    )


def farewell() -> None:
    return (
        "\fFarewell, my brave Hobbits. My work is now finished. "
        "Here at last, on the shores of the sea... "
        "comes the end of our Fellowship."
    )


def some_error_happened() -> None:
    return "I will not say: do not weep; for not all tears are an evil. "
