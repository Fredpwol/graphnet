#TODO: create exception for handling invalid refrence attribute
class Error(Exception):
    pass

class InvalidNodeTypeError(Error):
    pass


class MaxNodeError(Error):
    pass


class GraphTypeError(Error):
    pass

class MaxEdgeError(Error):
    pass