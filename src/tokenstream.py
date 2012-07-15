class TokenStream(object):
    def __init__(self, token_stream):
        """token_stream is a list of tokens"""
        self._token_stream = token_stream
        self._current_index = 0

    def __iter__(self):
        return self

    def next(self):
        """Consumes and returns the next token in the stream
        """
        try:
            cur_token = self._token_stream[self._current_index]
        except IndexError:
            raise StopIteration
        self._current_index += 1
        return cur_token

    def current(self):
        """Returns the token returned by the most recent call to next()
        """
        try:
            return self._token_stream[self._current_index-1]
        except IndexError:
            raise StopIteration

    def peek_ahead(self):
        """Returns the next token in the stream without consuming it
        """
        try:
            return self._token_stream[self._current_index]
        except IndexError:
            raise StopIteration

    def __repr__(self):
        return repr(self._token_stream)
