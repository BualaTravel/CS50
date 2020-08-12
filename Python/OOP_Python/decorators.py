#decorators add extra functionality to functions
#decorators are functions that take a function as input and returns a modified version of that function as output
# this is know as a functional programming paradigm. Where functions are themselves as values

def announce(f):
    def wrapper():
        print("About to run the function")
        f()
        print("Done with the function")
    return wrapper

@announce
def hello():
    print("Hello world!")

hello()
