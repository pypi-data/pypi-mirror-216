class LazyResultList:
    """
    A lazy list that wraps a MongoDB cursor and caches results as they are fetched.
    """
    def __init__(self, cursor, doc_class=None):
        self.cursor = cursor
        self.doc_class = doc_class
        self._cache = []

    def __getitem__(self, index):
        if index < 0:
            raise NotImplementedError('Negative indices are not supported')
        if isinstance(index, slice):
            return [self._getitem(i) for i in range(*index.indices(len(self)))]
        elif isinstance(index, int):
            return self._getitem(index)
        else:
            raise TypeError("indices must be integers or slices")

    def _getitem(self, index):
        if isinstance(index, int):
            while len(self._cache) <= index:
                try:
                    if self.doc_class:
                        self._cache.append(self.doc_class(next(self.cursor)))
                    else:
                        self._cache.append(next(self.cursor))
                except StopIteration:
                    raise IndexError('LazyList index out of range')
            return self._cache[index]
        else:
            raise TypeError("indices must be integers or slices")
        
    def __repr__(self):
        return "LazyList({!r})".format(self.cursor)
    
    def __iter__(self):
        for i in range(len(self._cache)):
            yield self._cache[i]
        for item in self.cursor:
            self._cache.append(item)
            yield item
            
    def first(self):
        return self[0]
    
    def next(self):
        """
        Fetch the next item from the MongoDB cursor.
        """
        try:
            item = next(self.cursor)
        except StopIteration:
            raise StopIteration("No more items in the list.")
            
        self._cache.append(item)
        return item